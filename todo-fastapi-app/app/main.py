from fastapi import FastAPI

app = FastAPI()

from app.db.posts import posts
from app.models.post_model import Post


@app.get("/health_check")
def root():
    return {"message": "Hello World"}


@app.get("/")
def get_all_posts(priority: int | None = None):
    if priority:
        return [post for post in posts if post["priority"] == priority]
    return posts


@app.get("/{id}")
def get_post_by_id(id: int):
    return list(filter(lambda post: post["id"] == id, posts))


@app.post("/")
def create_post(post: Post):
    posts.append(dict(post))
    return post


@app.put("/")
def update_post():
    return {"message": "Hello World"}


@app.delete("/")
def delete_post():
    return {"message": "Hello World"}
