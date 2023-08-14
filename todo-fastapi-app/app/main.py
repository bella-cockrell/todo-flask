from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import requests
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth
from getpass import getpass

# import db models
from app.db import db_models

# import db connection
from app.db.database import SessionLocal, engine

# import gateways
from app.gateways.users_gateway import create_user, get_user_by_username

# import auth
from app.helpers.oauth2 import create_access_token, verify_password

# import domain_models
from app.schemas.token_schema import Token, TokenData
from app.schemas.user_schema import User, UserCreate, UserInDB

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

github_url = "https://api.github.com"
github_url_invalid = "https://api.github.com/invalid"
github_url_repos = "https://api.github.com/search/repositories"


# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# randomly generated key
SECRET_KEY = "402af2408c510819c72aef58836c6a7e12e9af0c1a21bfa45c14dd20ef869563"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def authenticate_user(email: str, password: str, db: Session) -> UserInDB | bool:
    user = get_user_by_username(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
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
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def return_hello_world():
    return {"message": "Hello World"}

@app.get("/")
async def hello_world() -> dict:
    result = await return_hello_world()
    return result


@app.get("/test_req")
async def test_request() -> dict | None:
    try:
        res = requests.get(
            github_url_repos,
            params={"q": "requests+language:python"},
            headers={"Accept": "application/vnd.github.v3.text-match+json"},
        )
        res.raise_for_status()
    except HTTPError as http_err:
        print({f"HTTPError: {http_err}"})
    except Exception as ex:
        print({f"Exception: {ex}"})
    else:
        return res.json()


@app.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db=db, email=form_data.username, password=form_data.password
    )
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


@app.get("/users/me", response_model=User)
def read_users_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user


@app.post("/users", response_model=User)
async def create_new_user(
    user: UserCreate, db: Session = Depends(get_db)
) -> db_models.UserDbModel:
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

    # @app.get("/posts", response_model=list[Post])
    # def get_posts(
    #     priority: Annotated[
    #         int | None,
    #         Query(
    #             title="Priority integer",
    #             description="Priority integer for the urgency of the post item. The lower the number, the more urgent the item is.",
    #             ge=1,
    #         ),
    #     ] = None,
    #     response_description="All created posts",
    #     skip: int = 0,
    #     limit: int = 100,
    #     db: Session = Depends(get_db),
    # ) -> list[Post]:
    # #     if priority:
    # #         db_posts = get_posts_by_priority(db=db, priority=priority)
    # #         if db_posts is None:
    # #             raise HTTPException(status_code=404, detail="Post not found")
    # #         return db_posts
    # #     db_posts = get_all_posts(db=db, skip=skip, limit=limit)
    # #     if db_posts is None:
    # #         raise HTTPException(status_code=404, detail="Post not found")
    # #     return db_posts
    # #     # if priority:
    # #     #     return [post for post in posts if post.priority == priority]
    # #     # return posts

    # @app.get("/posts/{id}")
    # def get_post_by_id(
    #     id: Annotated[int, Path(title="The ID of the todo post", ge=1)]
    # ) -> list[Post]:
    #     return list(filter(lambda post: post.id == id, posts))

    # @app.post("/users/{user_id}/posts", response_model=Post)
    # def create_new_post(
    #     user_id: int, post_req: PostCreate, db: Session = Depends(get_db)
    # ) -> Post:
    #     # result = create_post(db=db, post=post_req, user_id=user_id)
    #     # print(result)
    #     pass

    #     # already_exists = list(filter(lambda post: post_req.id == post.id, posts))
    #     # if len(already_exists) >= 1:
    #     #     raise HTTPException(status_code=400, detail="Post already created")
    #     # posts.append(post_req)
    #     # created_post_index = posts.index(post_req)
    #     # created_post = posts[created_post_index]
    #     # return created_post

    # @app.put("/posts")
    # def update_post(put_req: Post) -> Post:
    #     found_post = list(filter(lambda post: put_req.id == post.id, posts))
    #     if len(found_post) == 0:
    #         raise HTTPException(status_code=404, detail="PostModel not found")
    #     index_of_found_post = posts.index(found_post[0])
    #     posts[index_of_found_post] = put_req
    #     return posts[index_of_found_post]

    # @app.delete("/posts", status_code=status.HTTP_200_OK)
    # def delete_post(
    #     id: Annotated[int, Path(title="The ID of the todo post", ge=1)]
    # ) -> None:
    found_post = list(filter(lambda post: post.id == id, posts))
    if len(found_post) == 0:
        raise HTTPException(status_code=404, detail="PostModel not found")
    else:
        posts.remove(found_post[0])
