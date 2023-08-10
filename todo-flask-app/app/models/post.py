import datetime as dt


class Post:
    def __init__(self, id: int, description: str, priority: int):
        self.id = id
        self.title = ""
        self.description = description
        self.priority = priority
        # self.created_at = dt.datetime.now()
