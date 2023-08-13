from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Path, Query, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.db.fake_users_db import fake_users_db
from app.db.posts import posts
from app.models.post_model import PostModel
from app.models.token_model import TokenDataModel, TokenModel
from app.models.user_models import UserInDBModel, UserModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# randomly generated key
SECRET_KEY = "402af2408c510819c72aef58836c6a7e12e9af0c1a21bfa45c14dd20ef869563"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_user(db, username: str | None) -> UserInDBModel | None:
    if username in db:
        user_dict = db[username]
        return UserInDBModel(**user_dict)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(fake_db, username: str, password: str) -> UserInDBModel | bool:
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def fake_decode_token(token) -> UserInDBModel | None:
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


def fake_hash_password(password: str):
    return "fakehashed" + password


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenDataModel(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=TokenModel)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},  # pyright: ignore
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
def read_users_me(current_user: Annotated[UserModel, Depends(get_current_active_user)]):
    return current_user


@app.get("/health_check")
def root():
    return {"message": "Hello World"}


@app.get("/")
def get_all_posts(
    priority: Annotated[
        int | None,
        Query(
            title="Priority integer",
            description="Priority integer for the urgency of the post item. The lower the number, the more urgent the item is.",
            ge=1,
        ),
    ] = None,
    response_description="All created posts",
) -> list[PostModel]:
    if priority:
        return [post for post in posts if post.priority == priority]
    return posts


@app.get("/{id}")
def get_post_by_id(
    id: Annotated[int, Path(title="The ID of the todo post", ge=1)]
) -> list[PostModel]:
    return list(filter(lambda post: post.id == id, posts))


@app.post("/")
def create_post(post_req: PostModel) -> PostModel:
    already_exists = list(filter(lambda post: post_req.id == post.id, posts))
    if len(already_exists) >= 1:
        raise HTTPException(status_code=400, detail="User already created")
    posts.append(post_req)
    created_post_index = posts.index(post_req)
    created_post = posts[created_post_index]
    return created_post


@app.put("/")
def update_post(put_req: PostModel) -> PostModel:
    found_post = list(filter(lambda post: put_req.id == post.id, posts))
    if len(found_post) == 0:
        raise HTTPException(status_code=404, detail="PostModel not found")
    index_of_found_post = posts.index(found_post[0])
    posts[index_of_found_post] = put_req
    return posts[index_of_found_post]


@app.delete("/", status_code=status.HTTP_200_OK)
def delete_post(
    id: Annotated[int, Path(title="The ID of the todo post", ge=1)]
) -> None:
    found_post = list(filter(lambda post: post.id == id, posts))
    if len(found_post) == 0:
        raise HTTPException(status_code=404, detail="PostModel not found")
    else:
        posts.remove(found_post[0])
