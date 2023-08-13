from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Path, Query, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

# import dbs
from app.db.fake_users_db import fake_users_db
from app.db.posts import posts
# import domain_models
from app.domain_models.post_domain_model import PostDomainModel
from app.domain_models.token_domain_model import (TokenDataDomainModel,
                                                  TokenDomainModel)
from app.domain_models.user_domain_model import (UserDomainModel,
                                                 UserInDBDomainModel)
# import gateways
from app.gateways.users_gateway import get_user
# import auth
from app.helpers.oauth2 import create_access_token, verify_password

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# randomly generated key
SECRET_KEY = "402af2408c510819c72aef58836c6a7e12e9af0c1a21bfa45c14dd20ef869563"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def authenticate_user(
    fake_db, username: str, password: str
) -> UserInDBDomainModel | bool:
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


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
        token_data = TokenDataDomainModel(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/token", response_model=TokenDomainModel)
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
def read_users_me(current_user: Annotated[UserDomainModel, Depends(get_current_user)]):
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
) -> list[PostDomainModel]:
    if priority:
        return [post for post in posts if post.priority == priority]
    return posts


@app.get("/{id}")
def get_post_by_id(
    id: Annotated[int, Path(title="The ID of the todo post", ge=1)]
) -> list[PostDomainModel]:
    return list(filter(lambda post: post.id == id, posts))


@app.post("/")
def create_post(post_req: PostDomainModel) -> PostDomainModel:
    already_exists = list(filter(lambda post: post_req.id == post.id, posts))
    if len(already_exists) >= 1:
        raise HTTPException(status_code=400, detail="User already created")
    posts.append(post_req)
    created_post_index = posts.index(post_req)
    created_post = posts[created_post_index]
    return created_post


@app.put("/")
def update_post(put_req: PostDomainModel) -> PostDomainModel:
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
