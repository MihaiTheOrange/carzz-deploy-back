from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Image
from typing import List


import os
import shutil

router = APIRouter(
    prefix = '/images',
    tags = ['announcement_images']
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
async def upload_image(announcement_id:int, files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
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
    images = db.query(Image).filter(Image.announcement_id == announcement_id).all()
    image_urls = [f"/{UPLOAD_DIR}/{image.filename}" for image in images]
    return {"image_urls": image_urls}

