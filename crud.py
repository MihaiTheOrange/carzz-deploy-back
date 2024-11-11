from datetime import datetime, timezone
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import os


from models import Users, Image, Favorite

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


def update_user_theme(db: Session, user: models.Users, theme: schemas.UserThemeUpdate):
    fields = [field for field in dir(theme) if not field.startswith("_")]
    for field in fields:
        value = getattr(theme, field)
        setattr(user, field, value)
    db.commit()
    db.refresh(user)

    return user


def create_announcement(db: Session, announcement: schemas.AnnouncementCreate, user_id: int):
    try:
        # Create a new announcement instance
        db_announcement = models.Announcements(
            **announcement.model_dump(),  # Using `model_dump` instead of `dict`
            user_id=user_id, 
            created_at=datetime.now(timezone.utc),  # Using timezone-aware datetime
            views=0, 
            favs=0
        )
        
        # Add the announcement to the session and commit
        db.add(db_announcement)
        db.commit()
        
        # Refresh the session to retrieve the new announcement data
        db.refresh(db_announcement)
        
        return db_announcement

    except Exception as e:
        # Rollback the session in case of error
        db.rollback()
        
        # Raise an HTTPException with a status code and error details
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the announcement: {str(e)}")


def get_announcement_images(announcement_id, base_url, db: Session):
    announcement = db.query(models.Announcements).filter(models.Announcements.id == announcement_id).first()
    if announcement is None:
        raise HTTPException(status_code=404, detail="Anunțul nu a fost găsit")

    images = db.query(Image).filter(Image.announcement_id == announcement_id).all()
    data = []

    for image in images:
        data.append(f"{base_url}{UPLOAD_DIR}/{image.filename}")
    if not data:
        data.append(f"{base_url}{UPLOAD_DIR}/fd02d0d1-2cae-4813-b746-b5574964578e.jfif")
    return data


def get_user_phone(user_id, db: Session):
    user = db.query(Users).filter(Users.id == user_id).first()
    return user.phone_number


def get_announcements(db: Session, base_url):
    announcements = db.query(models.Announcements).all()
    for announcement in announcements:
        user = db.query(Users).filter(Users.id == announcement.user_id).first()
        announcement.user_phone_number = user.phone_number
        images = get_announcement_images(announcement.id, base_url, db)
        announcement.image_url = images
    return reversed(announcements)


def get_my_announcements(db: Session, user_id: int, base_url, skip: int = 0, limit: int = 1000):
    announcements = db.query(models.Announcements).filter(models.Announcements.user_id == user_id).offset(skip).limit(limit).all()
    for announcement in announcements:
        user = db.query(Users).filter(Users.id == announcement.user_id).first()
        announcement.user_phone_number = user.phone_number
        announcement.image_url = get_announcement_images(base_url=base_url, db=db, announcement_id=announcement.id)
    return reversed(announcements)


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


def delete_all_favorite(db: Session, announcement_id: int):
    db.query(Favorite).filter(Favorite.announcement_id == announcement_id).delete()


def delete_announcement(db: Session, announcement_id: int):
    delete_images(db, announcement_id)
    delete_all_favorite(db, announcement_id)
    db_announcement = db.query(models.Announcements).filter(models.Announcements.id == announcement_id).first()
    db.delete(db_announcement)
    db.commit()


def delete_images(db: Session, announcement_id: int):
    db_image = db.query(models.Image).filter(models.Image.announcement_id == announcement_id).all()
    for image in db_image:
        image_path = os.path.join(UPLOAD_DIR, image.filename)
        if os.path.exists(image_path):
            os.remove(image_path)
    db.query(Image).filter(Image.announcement_id == announcement_id).delete()


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


def read_favorites(db:Session, id: int, base_url):
    favorite_announcements = db.query(models.Announcements).filter(models.Announcements.id==models.Favorite.announcement_id, models.Favorite.user_id == id).all()
    for announcement in favorite_announcements:
        user = db.query(Users).filter(Users.id == announcement.user_id).first()
        announcement.user_phone_number = user.phone_number
        announcement.image_url = get_announcement_images(base_url=base_url, db=db, announcement_id=announcement.id)
    return reversed(favorite_announcements)


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


def add_interaction(db: Session, user_id, announcement_id):
    interaction_model = models.ViewedAnnouncements(
        user_id=user_id,
        announcement_id=announcement_id
    )
    db.add(interaction_model)
    db.commit()


