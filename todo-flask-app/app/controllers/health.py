from flask import Blueprint, Response, jsonify

health_blueprint = Blueprint("health_blueprint", __name__)


@health_blueprint.get("/health_check")
def health_check() -> tuple[Response, int]:
    return jsonify("Hello, world!"), 200
