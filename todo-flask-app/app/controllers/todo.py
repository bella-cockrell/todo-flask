from flask import Blueprint, Response, jsonify, redirect, request, url_for
from marshmallow import ValidationError

from app.db.db import posts
from app.models.post import Post
from app.validation.post import PostSchema

todo_blueprint = Blueprint("todo_blueprint", __name__)


@todo_blueprint.get("/")
def get_all_posts() -> Response:
    schema = PostSchema(many=True)

    #TODO: validation for query string
    if request.args.get("priority"):
        result = []
        for post in posts:
            if post.priority == request.args.get("priority", type=int):
                result.append(post)
                return schema.dump(result), 200
            else:
                return schema.dump(result), 200
    else:
        return schema.dump(posts), 200


@todo_blueprint.get("/<int:id>")
def get_post(id: int) -> Response:
    schema = PostSchema()
    result = list(filter(lambda post: post.id == id, posts))
    if len(result)== 0:
        return redirect("not_found")
    else:
        return schema.dump(result[0])


@todo_blueprint.post("/<int:id>")
def create_post(id: int) -> Response:
    create_request_data = request.json
    schema = PostSchema()

    try:
        result: Post = schema.load(create_request_data)
        print(f"result: {result}")
    except ValidationError as err:
        return jsonify(err.messages, 400)

    posts.append(result)

    response_data = schema.dump(result)
    return response_data, 201


@todo_blueprint.put("/<int:id>")
def update_post(id: int) -> Response:
    update_request_data = request.json
    schema = PostSchema()

    try:
        result: Post = schema.load(update_request_data)
    except ValidationError as err:
        return jsonify(err.messages, 400)

    found_post = list(filter(lambda post: post.id == result.id, posts))
    index_of_found_post = posts.index(found_post[0])

    if len(found_post) == 0:
        return redirect("not_found")
    else:
        posts[index_of_found_post] = result
        return redirect(url_for("todo_blueprint.get_post", id=id), 201)



@todo_blueprint.delete("/<int:id>")
def delete_post(id: int) -> Response:
    found_post = list(filter(lambda post: post.id == id, posts))

    if len(found_post) == 0:
        return redirect("not_found")
    else:
        posts.remove(found_post[0])
        return redirect("get_all_posts"), 201


@todo_blueprint.errorhandler(404)
def not_found(error: int | Exception) -> Response:
    return f"<p>{error}</p>", 404
