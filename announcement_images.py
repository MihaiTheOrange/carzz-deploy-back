from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Image
from typing import List
from models import Announcements
from schemas import ImageUpload
import os
import shutil
import auth
import uuid
import base64
import io

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


'''@router.post("/upload/")
async def upload_image(announcement_id: int, files: List[UploadFile] = File(...), db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    announcement = db.query(Announcements).filter(Announcements.id == announcement_id).first()

    if announcement is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if announcement.user_id != current_user.get('id'):
        raise HTTPException(status_code=403,
                            detail=f"User ID {current_user.get('id')} does not match the announcement user ID {announcement.user_id}")

    for uploaded_file in files:
        # Generate a unique name for the file
        unique_filename = str(uuid.uuid4()) + os.path.splitext(uploaded_file.filename)[1]

        with open(os.path.join(UPLOAD_DIR, unique_filename), "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)

        db_image = Image(filename=unique_filename)
        db_image.announcement_id = announcement_id
        db.add(db_image)

        db.commit()
    return {"message": "Images uploaded successfully"}
'''

@router.post("/post64")
async def upload_image(announcement_id: int, image: ImageUpload, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    announcement = db.query(Announcements).filter(Announcements.id == announcement_id).first()

    if announcement is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if announcement.user_id != current_user.get('id'):
        raise HTTPException(status_code=403,
                            detail=f"User ID {current_user.get('id')} does not match the announcement user ID {announcement.user_id}")

    try:
        image_data = base64.b64decode(image.content)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image data") from e

    unique_filename = str(uuid.uuid4()) + os.path.splitext(image.file_name)[1]
    with open(os.path.join(UPLOAD_DIR, unique_filename), "wb") as buffer:
        buffer.write(image_data)
    db_image = Image(filename=unique_filename)
    db_image.announcement_id = announcement_id
    db.add(db_image)
    db.commit()
    return {"message": "Image uploaded successfully"}


@router.get("/getimage/{announcement_id}")
async def get_announcement_image(announcement_id, db: Session = Depends(get_db)):
    announcement = db.query(Announcements).filter(Announcements.id == announcement_id).first()
    if announcement is None:
        raise HTTPException(status_code=404, detail="Product not found")

    images = db.query(Image).filter(Image.announcement_id == announcement_id).all()
    data = []
    for image in images:
        data.append({'id': image.id, 'image_url': f"/{UPLOAD_DIR}/{image.filename}"})
    return data


@router.get("/getfirstimage/{announcement_id}")
async def get_announcement_first_image(announcement_id, db: Session = Depends(get_db)):
    announcement = db.query(Announcements).filter(Announcements.id == announcement_id).first()
    if announcement is None:
        raise HTTPException(status_code=404, detail="Product not found")

    image = db.query(Image).filter(Image.announcement_id == announcement_id).first()
    data = {'id': image.id, 'image_url': f"/{UPLOAD_DIR}/{image.filename}"}
    return data


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