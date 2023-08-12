from app.models.post_model import PostModel

posts = [
    PostModel(id=1, description="hello", priority=1, title="It's me"),
    PostModel(id=2, description="hello again", priority=2, title="It's me 2"),
    PostModel(id=3, description="last minute prio", priority=1),
]

# posts = [
#     {"id": 1, "description": "hello", "priority": 1},
#     {"id": 2, "description": "hello again", "priority": 2},
#     {"id": 3, "description": "last minute prio", "priority": 1},
# ]
