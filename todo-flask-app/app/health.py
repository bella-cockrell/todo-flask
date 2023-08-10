from flask import Blueprint, Response

health_blueprint = Blueprint("health_blueprint", __name__)


@health_blueprint.get("/healthcheck")
def healthcheck() -> Response:
    return "<p>Hello, World! ❤️</p>", 200
