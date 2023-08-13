from sqlalchemy.orm import Session

from app.db import db_models
from app.domain_models import post_domain_model, user_domain_model
from app.domain_models.user_domain_model import UserInDBDomainModel
from app.helpers.oauth2 import get_password_hash


def get_user(db, username: str | None) -> UserInDBDomainModel | None:
    if username in db:
        user_dict = db[username]
        return UserInDBDomainModel(**user_dict)


# This is SqlAlchemy, not core Python
def get_user_by_id(db: Session, user_id: int) -> db_models.UserDbModel | None:
    return (
        db.query(db_models.UserDbModel)
        .filter(db_models.UserDbModel.id == user_id)
        .first()
    )


def get_user_by_email(db: Session, email: str) -> db_models.UserDbModel | None:
    return (
        db.query(db_models.UserDbModel)
        .filter(db_models.UserDbModel.email == email)
        .first()
    )


def get_all_users(
    db: Session, skip: int = 0, limit: int = 100
) -> list[db_models.UserDbModel]:
    return db.query(db_models.UserDbModel).offset(skip).limit(limit).all()


def create_user(
    db: Session, user: user_domain_model.UserCreate
) -> db_models.UserDbModel:
    hashed_password = get_password_hash(user.password)
    db_user = db_models.UserDbModel(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_posts(
    db: Session, skip: int = 0, limit: int = 100
) -> list[db_models.PostDbModel]:
    return db.query(db_models.PostDbModel).offset(skip).limit(limit).all()


def create_post(
    db: Session, post: post_domain_model.PostCreateDomainModel, user_id: int
) -> db_models.PostDbModel:
    db_post = db_models.PostDbModel(**post, owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
