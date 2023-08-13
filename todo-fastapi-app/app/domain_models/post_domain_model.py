from datetime import datetime, timezone

from pydantic import BaseModel, Field

class PostBaseDomainModel(BaseModel):
    description: str = Field(description="The body text of the post")
    title: str | None = Field(default=None, description="Optional title of the post")
    priority: int = Field(gt=0, description="Priority must be greater than 0")
    created_at: datetime = Field(
        default=datetime.now(timezone.utc), description="Time of post creation"
    )

class PostCreateDomainModel():
    pass

class PostDomainModel(PostBaseDomainModel):
    # UUID maybe generated instead?
    id: int = Field(
        gt=0,
        title="The unique ID of the item",
        description="The ID must be greater than 0",
    )
    owner_id: int

    class Config:
        orm_mode = True

