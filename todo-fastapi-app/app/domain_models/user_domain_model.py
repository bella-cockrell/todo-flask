from pydantic import BaseModel


class UserDomainModel(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDBDomainModel(UserDomainModel):
    hashed_password: str
