from sqlalchemy.orm import Session

from app.db.db_models import PostDbModel
from app.schemas.post_schema import PostCreate


def get_all_posts(db: Session, skip: int = 0, limit: int = 100) -> list[PostDbModel]:
    return db.query(PostDbModel).offset(skip).limit(limit).all()


def create_post(db: Session, post: PostCreate, user_id: int) -> PostDbModel:
    db_post = PostDbModel(**post, owner_id=user_id)  # pyright: ignore
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
