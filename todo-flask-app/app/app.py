from flask import Flask

from app.controllers.health import health_blueprint
from app.controllers.todo import todo_blueprint

app = Flask(__name__)

app.register_blueprint(health_blueprint)
app.register_blueprint(todo_blueprint)
