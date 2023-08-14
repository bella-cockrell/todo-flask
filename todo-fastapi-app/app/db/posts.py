from app.schemas.post_schema import Post

posts = [
    Post(id=1, description="hello", priority=1, title="It's me", owner_id=1),
    Post(id=2, description="hello again", priority=2, title="It's me 2", owner_id=1),
    Post(id=3, description="last minute prio", priority=1, owner_id=1),
]

# posts = [
#     {"id": 1, "description": "hello", "priority": 1},
#     {"id": 2, "description": "hello again", "priority": 2},
#     {"id": 3, "description": "last minute prio", "priority": 1},
# ]
