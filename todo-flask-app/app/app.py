from flask import Flask

from .health import health_blueprint
from .todo import todo_blueprint

app = Flask(__name__)

app.register_blueprint(health_blueprint)
app.register_blueprint(todo_blueprint)
