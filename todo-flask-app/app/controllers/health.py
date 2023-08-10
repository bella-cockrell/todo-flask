from flask import Blueprint, Response

health_blueprint = Blueprint("health_blueprint", __name__)


@health_blueprint.get("/health_check")
def health_check() -> Response:
    return "<p>Hello, World! ❤️</p>", 200
