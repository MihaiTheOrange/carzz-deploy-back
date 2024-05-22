from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

import models
import schemas
from models import Users, Image
import os
from announcement_images import UPLOAD_DIR


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
    db_announcement = models.Announcements(**announcement.dict(), user_id=user_id, created_at=datetime.now().strftime("%H:%M %Y-%m-%d"), views=0, favs=0)
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement


def get_announcements(db: Session, skip: int = 0, limit: int = 10):
    announcements = db.query(models.Announcements).offset(skip).limit(limit).all()
    for announcement in announcements:
        user = db.query(Users).filter(Users.id == announcement.user_id).first()
        announcement.user_phone_number = user.phone_number
        image = db.query(Image).filter(Image.announcement_id == announcement.id).first()
        if image:
            image_url = f"/{UPLOAD_DIR}/{image.filename}"
        else:
            image_url = ''
        announcement.image_url = image_url
    return announcements


def get_my_announcements(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    announcements = db.query(models.Announcements).filter(models.Announcements.user_id == user_id).offset(skip).limit(limit).all()
    for announcement in announcements:
        user = db.query(Users).filter(Users.id == announcement.user_id).first()
        announcement.user_phone_number = user.phone_number
    return announcements


def get_announcement(db: Session, announcement_id: int):
    announcement = db.query(models.Announcements).filter(models.Announcements.id == announcement_id).first()
    if announcement is None:
        return None
    user = db.query(Users).filter(Users.id == announcement.user_id).first()
    announcement.user_phone_number = user.phone_number
    return announcement


def add_view(db: Session, announcement_id: int):
    announcement = db.query(models.Announcements).filter(models.Announcements.id == announcement_id).first()
    announcement.views += 1
    db.commit()
    db.refresh(announcement)


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
    delete_images(db, announcement_id)


def delete_images(db: Session, announcement_id: int):
    db_image = db.query(models.Image).filter(models.Image.announcement_id == announcement_id).all()
    for image in db_image:
        db.delete(image)
        image_path = os.path.join(UPLOAD_DIR, image.filename)
        if os.path.exists(image_path):
            os.remove(image_path)


def add_favorite(db: Session, favorite: int, id: int):
    favorite_model = models.Favorite(
        user_id=id,
        announcement_id=favorite
    )
    db.add(favorite_model)
    db.commit()
    return f'Anunțul {favorite_model.announcement_id} a fost adăugat'


def add_fav_db(db: Session, announcement_id: int):
    announcement = db.query(models.Announcements).filter(models.Announcements.id == announcement_id).first()
    announcement.favs += 1
    db.commit()
    db.refresh(announcement)


def read_favorites(db:Session, id: int):
    favorite_announcements = db.query(models.Announcements).filter(models.Announcements.id==models.Favorite.announcement_id, models.Favorite.user_id == id).all()
    for announcement in favorite_announcements:
        user = db.query(Users).filter(Users.id == announcement.user_id).first()
        announcement.user_phone_number = user.phone_number
    return favorite_announcements


def get_favorite(db: Session, id: int, announcement_id: int):
    return db.query(models.Favorite).filter(models.Favorite.announcement_id == announcement_id,
                                            models.Favorite.user_id == id).first()


def delete_favorite(db: Session, announcement_id: int, id: int):
    db_announcement = db.query(models.Favorite).filter(models.Favorite.announcement_id == announcement_id,
                                                       models.Favorite.user_id == id).first()
    db.delete(db_announcement)
    db.commit()


def remove_fav_db(db: Session, announcement_id: int):
    announcement = db.query(models.Announcements).filter(models.Announcements.id == announcement_id).first()
    if announcement:
        announcement.favs -= 1
        db.commit()
        db.refresh(announcement)


def create_rating(db: Session, user_id: int, rating: schemas.SellerRatingCreate):
    db_rating = models.SellerRating(**rating.dict(), user_id=user_id, created_at=datetime.now().strftime("%H:%M %Y-%m-%d"))
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating


def get_rating(db: Session,rating_id: int):
    return db.query(models.SellerRating).filter(models.SellerRating.id == rating_id).first()


def get_my_writen_ratings(db: Session, user_id: int):
    return db.query(models.SellerRating).filter(models.SellerRating.user_id == user_id).all()


def get_seller_ratings(db: Session, seller_id: int):
    return db.query(models.SellerRating).filter(models.SellerRating.seller_id == seller_id).all()


def update_rating(db: Session, rating: schemas.SellerRating, rating_update: schemas.SellerRatingUpdate):
    for key, value in rating_update.dict().items():
        setattr(rating, key, value)
    db.commit()
    db.refresh(rating)
    return rating


def delete_rating(db: Session, rating_id: int):
    db_rating = db.query(models.SellerRating).filter(models.SellerRating.id == rating_id).first()
    db.delete(db_rating)
    db.commit()
