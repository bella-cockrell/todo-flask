from pydantic import BaseModel

from app.schemas.post_schema import Post


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    full_name: str | None = None
    posts: list[Post] = []

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str
