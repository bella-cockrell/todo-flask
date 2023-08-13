from pydantic import BaseModel


class TokenDomainModel(BaseModel):
    access_token: str
    token_type: str


class TokenDataDomainModel(BaseModel):
    username: str | None = None
