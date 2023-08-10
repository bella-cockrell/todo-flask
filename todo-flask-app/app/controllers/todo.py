from flask import Blueprint, Response, redirect, request, url_for

from app.db.db import posts

todo_blueprint = Blueprint("todo_blueprint", __name__)


@todo_blueprint.get("/")
def get_all_posts() -> Response:
    if request.args.get("priority"):
        result = []
        for post in posts:
            if post["priority"] == request.args.get("priority", type=int):
                result.append(post)
            else:
                continue
        return result
    else:
        return posts, 200


@todo_blueprint.get("/<int:id>")
def get_post(id: int) -> Response:
    return [post for post in posts if post["id"] == id], 200


@todo_blueprint.post("/<int:id>")
def create_post(id: int) -> Response:
    new_post = request.json
    posts.append(new_post)
    return redirect(url_for("get_post", id=id), 201)


@todo_blueprint.put("/<int:id>")
def update_post(id: int) -> Response:
    updated_post = request.json
    for post in posts:
        if post["id"] == id:
            post.update(updated_post)
        else:
            continue
    return redirect(url_for("get_post", id=id), 201)


@todo_blueprint.delete("/<int:id>")
def delete_post(id: int) -> Response:
    for post in posts:
        if post["id"] == id:
            posts.remove(post)
        else:
            continue
    return posts, 204


@todo_blueprint.errorhandler(404)
def not_found(error: int | Exception) -> Response:
    return f"<p>{error}</p>", 404
