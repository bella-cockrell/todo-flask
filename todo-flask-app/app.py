from flask import Flask, Response, request, redirect, url_for

posts = [{"id": 1, "description": "hello", "priority": 1}, 
         {"id": 2, "description": "hello again", "priority": 2}]

app = Flask(__name__)

@app.get("/healthcheck")
def healthcheck() -> Response:
    return "<p>Hello, World! ❤️</p>", 200

@app.get("/")
def get_all_posts() -> Response:
    if request.args.get('priority'):
        result = []
        for post in posts:
            if post["priority"] == request.args.get('priority', type=int):
                result.append(post)
            else:
                continue
        return result
    else:
        return posts, 200

@app.get("/<int:id>")
def get_post(id: int) -> Response:
    return [post for post in posts if post["id"] == id], 200

@app.post("/<int:id>")
def create_post(id: int) -> Response:
    new_post = request.json
    posts.append(new_post)
    return redirect(url_for("get_post", id=id), 201)

@app.put("/<int:id>")
def update_post(id: int) -> Response:
    updated_post = request.json
    for post in posts:
        if post["id"] == id:
            post.update(updated_post)
        else:
            continue    
    return redirect(url_for("get_post", id=id), 201)

@app.delete("/<int:id>")
def delete_post(id: int) -> Response:
    for post in posts:
        if post["id"] == id:
            posts.remove(post)
        else:
            continue
    return posts, 204

@app.errorhandler(404)
def not_found(error: int | Exception) -> Response:
    return f"<p>{error}</p>", 404