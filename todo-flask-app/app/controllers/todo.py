from flask import Blueprint, Response, jsonify, redirect, request, url_for
from marshmallow import ValidationError

from app.db.db import posts
from app.models.post import Post
from app.validation.post import PostSchema

todo_blueprint = Blueprint("todo_blueprint", __name__)


@todo_blueprint.get("/")
def get_all_posts() -> Response:
    schema = PostSchema(many=True)

    if request.args.get("priority"):
        result = []
        for post in posts:
            if post.priority == request.args.get("priority", type=int):
                result.append(post)
            else:
                continue
        return result
    else:
        return schema.dump(posts), 200


@todo_blueprint.get("/<int:id>")
def get_post(id: int) -> Response:
    schema = PostSchema()
    result = list(filter(lambda post: post.id == id, posts))
    return schema.dump(result[0])


@todo_blueprint.post("/<int:id>")
def create_post(id: int) -> Response:
    request_data = request.json
    schema = PostSchema()

    try:
        result: Post = schema.load(request_data)
        print(f"result: {result}")
    except ValidationError as err:
        return jsonify(err.messages, 400)

    posts.append(result)

    response_data = schema.dump(result)
    return response_data, 201


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
