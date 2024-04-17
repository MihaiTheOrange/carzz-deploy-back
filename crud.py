from typing import List

from sqlalchemy.orm import Session

import models
import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def update_user(db: Session, user: models.Users, user_update: schemas.UserUpdate):
    fields = [field for field in dir(user_update) if not field.startswith("_")]
    for field in fields:
        value = getattr(user_update, field)
        setattr(user, field, value)
    db.commit()
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


def get_my_announcements(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Announcements).filter(models.Announcements.user_id == user_id).offset(skip).limit(
        limit).all()


def get_announcement(db: Session, announcement_id: int):
    return db.query(models.Announcements).filter(models.Announcements.id == announcement_id).first()


def update_announcement(db: Session, announcement: models.Announcements,
                        announcement_update: schemas.AnnouncementUpdate):
    for key, value in announcement_update.dict().items():
        setattr(announcement, key, value)
    db.commit()
    db.refresh(announcement)
    return announcement


def delete_announcement(db: Session, announcement_id: int):
    db_announcement = db.query(models.Announcements).filter(models.Announcements.id == announcement_id).first()
    db.delete(db_announcement)
    db.commit()


def add_favorite(db: Session, favorite: schemas.Favorite, id: int):
    favorite_model = models.Favorite(
        user_id=id,
        announcement_id=favorite.announcement_id
    )
    db.add(favorite_model)
    db.commit()
    return f'Product {favorite_model.announcement_id} was added'


def read_favorites(db: Session, id: int):
    favorite_announcements = db.query(models.Announcements).filter(
        models.Announcements.id == models.Favorite.announcement_id, models.Favorite.user_id == id).all()
    return favorite_announcements


def get_favorite(db: Session, id: int, announcement_id: int):
    return db.query(models.Favorite).filter(models.Favorite.announcement_id == announcement_id,
                                            models.Favorite.user_id == id).first()


def delete_favorite(db: Session, announcement_id: int, id: int):
    db_announcement = db.query(models.Favorite).filter(models.Favorite.announcement_id == announcement_id,
                                                       models.Favorite.user_id == id).first()
    db.delete(db_announcement)
    db.commit()


def create_rating(db: Session, user_id: int, rating: schemas.SellerRatingCreate):
    db_rating = models.SellerRating(**rating.dict(), user_id=user_id)
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating


def get_my_writen_ratings(db: Session, user_id: int):
    return db.query(models.SellerRating).filter(models.SellerRating.user_id == user_id).all()


def get_seller_ratings(db: Session, seller_id: int):
    return db.query(models.SellerRating).filter(models.SellerRating.seller_id == seller_id).all()


def delete_rating(db: Session, seller_id: int, id: int):
    pass
