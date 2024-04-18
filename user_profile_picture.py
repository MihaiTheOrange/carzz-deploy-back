from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import ProfilePic
from typing import List
from models import Announcements

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


@router.post("/upload/")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    with open(os.path.join(UPLOAD_DIR, file.filename), "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        db_image = ProfilePic(filename=file.filename)
        db_image.user_id = current_user.get('id')
        db.add(db_image)
    db.commit()
    return {"message": "Image uploaded successfully"}
