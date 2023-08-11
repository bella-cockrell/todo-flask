from time import timezone
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class Post(BaseModel):
    id: int
    description: str
    title: str | None = None
    priority: int = Field(gt=0, description="Priority must be greater than 0")
    created_at: datetime = datetime.now(timezone.utc)
