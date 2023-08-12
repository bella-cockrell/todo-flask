from app.models.user_models import UserInDBModel


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDBModel(**user_dict)
