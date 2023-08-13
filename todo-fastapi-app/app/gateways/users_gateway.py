from app.domain_models.user_domain_model import UserInDBDomainModel


def get_user(db, username: str | None) -> UserInDBDomainModel | None:
    if username in db:
        user_dict = db[username]
        return UserInDBDomainModel(**user_dict)
