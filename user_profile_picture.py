from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import ProfilePic
from models import Users

import os
import shutil
import auth

router = APIRouter(
    prefix='/profilepic',
    tags=['profile_pictures']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


UPLOAD_DIR = "profile_pictures"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.put("/upload/")
async def upload_image(uploaded_file: UploadFile = File(...), db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    db_pic = db.query(ProfilePic).filter(ProfilePic.user_id == current_user.get('id')).first()
    if db_pic:
        image_path = os.path.join(UPLOAD_DIR, db_pic.filename)
        if os.path.exists(image_path):
            os.remove(image_path)
        with open(os.path.join(UPLOAD_DIR, uploaded_file.filename), "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)
        db_pic.filename = uploaded_file.filename
        db.commit()
    else:
        with open(os.path.join(UPLOAD_DIR, uploaded_file.filename), "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)
        db_image = ProfilePic(filename=uploaded_file.filename)
        db_image.user_id = current_user.get('id')
        db.add(db_image)
        db.commit()
    return {"message": "Imaginea a fost încărcată cu succes"}


@router.get("/get/{user_id}")
async def get_pfp(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Utilizatorul nu a fost găsit")

    pfp = db.query(ProfilePic).filter(ProfilePic.user_id == user_id).first()
    image_url = f"/{UPLOAD_DIR}/{pfp.filename}"
    return {"image_urls": image_url}


