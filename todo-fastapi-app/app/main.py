from typing import Annotated, List

import requests
from fastapi import FastAPI, HTTPException, Path, Query

app = FastAPI()

from app.db.posts import posts
from app.models.post_model import Post


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
    ] = None
) -> List[Post]:
    if priority:
        return [post for post in posts if post.priority == priority]
    return posts


@app.get("/{id}")
def get_post_by_id(
    id: Annotated[int, Path(title="The ID of the todo post", ge=1)]
) -> List[Post]:
    return list(filter(lambda post: post.id == id, posts))


@app.post("/")
def create_post(post_req: Post) -> List[Post]:
    already_exists = list(filter(lambda post: post_req.id == post.id, posts))
    if len(already_exists) >= 1:
        raise HTTPException(status_code=400, detail="User already created")
    posts.append(post_req)
    created_post = list(filter(lambda post: post_req.id == post.id, posts))
    return created_post


@app.put("/")
def update_post(put_req: Post) -> Post:
    found_post = list(filter(lambda post: put_req.id == post.id, posts))
    if len(found_post) == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    index_of_found_post = posts.index(found_post[0])
    posts[index_of_found_post] = put_req
    return posts[index_of_found_post]


@app.delete("/")
def delete_post(
    id: Annotated[int, Path(title="The ID of the todo post", ge=1)]
) -> None:
    found_post = list(filter(lambda post: post.id == id, posts))
    if len(found_post) == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        posts.remove(found_post[0])
