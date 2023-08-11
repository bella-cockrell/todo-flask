from pydantic import BaseModel, Field
import datetime


class Post(BaseModel):
    id: int
    description: str
    title: str | None = None
    priority: int = Field(gt=0, description="Priority must be greater than 0")
    created_at: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
