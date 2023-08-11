# for e2e testing - not best but works for now
from flask import Flask

from app.config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.config.from_pyfile("config.py")

    from app.controllers.health import health_blueprint
    from app.controllers.todo import todo_blueprint

    app.register_blueprint(health_blueprint)
    app.register_blueprint(todo_blueprint)

    return app
