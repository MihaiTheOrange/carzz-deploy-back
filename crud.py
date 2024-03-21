from sqlalchemy.orm import Session

import models
import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, password=user.password, full_name=user.full_name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
