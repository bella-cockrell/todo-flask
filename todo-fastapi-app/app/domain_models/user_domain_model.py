from pydantic import BaseModel

from app.domain_models.post_domain_model import PostDomainModel


class UserBaseDomain(BaseModel):
    email: str | None = None


class UserCreate(UserBaseDomain):
    password: str


class UserDomainModel(UserBaseDomain):
    id: int
    username: str
    full_name: str | None = None
    posts: list[PostDomainModel] = []

    class Config:
        orm_mode = True


class UserInDBDomainModel(UserDomainModel):
    hashed_password: str
