from app.models.post import Post

# posts = [
#     {"id": 1, "description": "hello", "priority": 1},
#     {"id": 2, "description": "hello again", "priority": 2},
# ]

posts = [
    Post(id=1, description="hello", priority=1),
    Post(id=2, description="hello again", priority=2),
]
