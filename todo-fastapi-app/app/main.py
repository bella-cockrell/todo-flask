from typing import Annotated
from flask import Response

import requests
from fastapi import Depends, FastAPI, HTTPException, Path, Query, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

from app.db.fake_users_db import fake_users_db
from app.db.posts import posts
from app.helpers.oauth2 import fake_decode_token, fake_hash_password
from app.models.post_model import PostModel
from app.models.user_models import UserInDBModel, UserModel


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
            # 401 should return header as part of spec
        )
    return user


def get_current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict:
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDBModel(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}
    #this is the only part that you need to be manually compliant with OpenAPI


@app.get("/users/me")
def read_users_me(
    current_user: Annotated[UserModel, Depends(get_current_active_user)]
):
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
