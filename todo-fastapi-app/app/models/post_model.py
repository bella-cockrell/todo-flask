from pydantic import BaseModel


class Post(BaseModel):
    id: int
    description: str
    title: str | None = None
    priority: int
