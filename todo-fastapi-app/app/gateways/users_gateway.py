from sqlalchemy.orm import Session

from app.db.db_models import UserDbModel
from app.domain_models.user_domain_model import UserInDBDomainModel, UserCreate
from app.helpers.oauth2 import get_password_hash


def get_user(db, username: str | None) -> UserInDBDomainModel | None:
    if username in db:
        user_dict = db[username]
        return UserInDBDomainModel(**user_dict)


# This is SqlAlchemy, not core Python
def get_user_by_id(db: Session, user_id: int) -> UserDbModel | None:
    return db.query(UserDbModel).filter(UserDbModel.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> UserDbModel | None:
    return db.query(UserDbModel).filter(UserDbModel.email == email).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> list[UserDbModel]:
    return db.query(UserDbModel).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> UserDbModel:
    hashed_password = get_password_hash(user.password)
    db_user = UserDbModel(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
