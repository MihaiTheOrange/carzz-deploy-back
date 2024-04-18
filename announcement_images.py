from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Image
from typing import List
from models import Announcements
from datetime import datetime

import os
import shutil
import auth

router = APIRouter(
    prefix='/images',
    tags=['announcement_images']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/")
async def upload_image(announcement_id:int, files: List[UploadFile] = File(...), db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    announcement = db.query(Announcements).filter(Announcements.id == announcement_id).first()

    if announcement is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if announcement.user_id != current_user.get('id'):
        raise HTTPException(status_code=403,
                            detail=f"User ID {current_user.get('id')} does not match the announcement user ID {announcement.id}")

    for uploaded_file in files:
        with open(os.path.join(UPLOAD_DIR, uploaded_file.filename), "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)
        db_image = Image(filename=uploaded_file.filename)
        db_image.announcement_id = announcement_id
        db.add(db_image)
    db.commit()
    return {"message": "Images uploaded successfully"}


@router.get("/getimage/{announcement_id}")
async def get_announcement_image(announcement_id, db: Session = Depends(get_db)):
    announcement = db.query(Announcements).filter(Announcements.id == announcement_id).first()
    if announcement is None:
        raise HTTPException(status_code=404, detail="Product not found")

    images = db.query(Image).filter(Image.announcement_id == announcement_id).all()
    image_urls = [f"/{UPLOAD_DIR}/{image.filename}" for image in images]
    return {"image_urls": image_urls}


@router.delete("/delete/{image_id}")
async def delete_image(image_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    db_image = db.query(Image).filter(Image.id == image_id).first()

    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")

    db_announcement = db.query(Announcements).filter(Announcements.id == db_image.announcement_id).first()
    image_user_id = db_announcement.user_id
    if current_user.get('id') != image_user_id:
        raise HTTPException(status_code=403,
                            detail="User id does not match announcement user id")

    # Delete the file from the filesystem
    image_path = os.path.join(UPLOAD_DIR, db_image.filename)
    if os.path.exists(image_path):
        os.remove(image_path)

    # Delete the image from the database
    db.delete(db_image)
    db.commit()

    return {"message": "Image deleted successfully"}

