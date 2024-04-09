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


def create_announcement(db: Session, announcement: schemas.AnnouncementCreate, user_id: int):
    db_announcement = models.Announcements(**announcement.dict(), user_id=user_id)
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement


def get_announcements(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Announcements).offset(skip).limit(limit).all()


def get_announcement(db: Session, announcement_id: int):
    return db.query(models.Announcements).filter(models.Announcements.id == announcement_id).first()


def update_announcement(db: Session, announcement: models.Announcements, announcement_update: schemas.AnnouncementUpdate):
    for key, value in announcement_update.dict().items():
        setattr(announcement, key, value)
    db.commit()
    db.refresh(announcement)
    return announcement


def delete_announcement(db: Session, announcement_id: int):
    db_announcement = db.query(models.Announcements).filter(models.Announcements.id == announcement_id).first()
    db.delete(db_announcement)
    db.commit()

def add_favorite(db: Session, favorite: schemas.Favorite, id):
    favorite_model=models.Favorite(
        user_id=id,
        announcement_id=favorite.announcement_id
    )
    db.add(favorite_model)
    db.commit()
    return f'product {favorite_model.announcement_id} was added'

def read_favorites(db:Session, id):
    favorite_announcements=db.query(models.Announcements).filter(models.Announcements.id==models.Favorite.announcement_id).all()
    return favorite_announcements
