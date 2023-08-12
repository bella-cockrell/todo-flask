from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDBModel(UserModel):
    hashed_password: str
