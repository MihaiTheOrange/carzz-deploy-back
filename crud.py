from sqlalchemy.orm import Session

import models
import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def update_user(db: Session, user: models.Users, user_update: schemas.UserUpdate):
    # Get the fields from the UserUpdate instance
    fields = [field for field in dir(user_update) if not field.startswith("_")]

    # Update the corresponding fields of the user instance
    for field in fields:
        value = getattr(user_update, field)
        setattr(user, field, value)

    # Commit changes to the database
    db.commit()

    # Refresh the user instance to reflect changes
    db.refresh(user)

    return user


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
