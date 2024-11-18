from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Path, Request, Form
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Image
from models import Announcements
from schemas import ImageUpload
import os
import auth
import uuid
import base64
from typing import List
import shutil
from SupaB import supabase, BUCKET_NAME

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


# @router.post("/upload/")
# async def upload_image(announcement_id: int = Form(...), files: List[UploadFile] = File(...),
#                        db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
#     # Check if the announcement exists
#     announcement = db.query(Announcements).filter(Announcements.id == announcement_id).first()
#
#     if announcement is None:
#         raise HTTPException(status_code=404, detail="Product not found")
#
#     if announcement.user_id != current_user.get('id'):
#         raise HTTPException(status_code=403,
#                             detail=f"User ID {current_user.get('id')} does not match the announcement user ID {announcement.user_id}")
#
#     # Process the uploaded files
#     for uploaded_file in files:
#         unique_filename = str(uuid.uuid4()) + os.path.splitext(uploaded_file.filename)[1]
#
#         # Save the file to disk
#         with open(os.path.join(UPLOAD_DIR, unique_filename), "wb") as buffer:
#             shutil.copyfileobj(uploaded_file.file, buffer)
#
#         # Save file information in the database
#         db_image = Image(filename=unique_filename)
#         db_image.announcement_id = announcement_id
#         db.add(db_image)
#         db.commit()
#
#     return {"message": "Images uploaded successfully"}


@router.post("/upload/")
async def upload_image(
        announcement_id: int = Form(...),
        files: List[UploadFile] = File(...),
        db: Session = Depends(get_db),
        current_user: dict = Depends(auth.get_current_user)
):
    # Check if the announcement exists
    announcement = db.query(Announcements).filter(Announcements.id == announcement_id).first()

    if announcement is None:
        raise HTTPException(status_code=404, detail="Announcement not found")

    if announcement.user_id != current_user.get('id'):
        raise HTTPException(status_code=403, detail="User not authorized for this announcement")

    uploaded_image_urls = []  # List to store URLs of uploaded images

    # Process the uploaded files
    for uploaded_file in files:
        unique_filename = f"{uuid.uuid4()}{os.path.splitext(uploaded_file.filename)[1]}"

        # Read file content
        file_content = await uploaded_file.read()

        # Upload the image to Supabase bucket
        response = supabase.storage.from_(BUCKET_NAME).upload(unique_filename, file_content)

        # Check if the response contains a valid path (upload successful)
        if not response.path:
            raise HTTPException(status_code=500, detail="Failed to upload image to Supabase storage")

        # Generate the public URL using the full_path (or path)
        image_url = supabase.storage.from_(BUCKET_NAME).get_public_url(response.path)

        # Save file information in the database
        db_image = Image(filename=image_url, announcement_id=announcement_id)
        db.add(db_image)
        db.commit()
        db.refresh(db_image)

        # Append the image URL to the response list
        uploaded_image_urls.append({"image_id": db_image.id, "image_url": image_url})

    return {"message": "Images uploaded successfully", "images": uploaded_image_urls}


@router.get("/getimage/{announcement_id}")
async def get_announcement_image(announcement_id, db: Session = Depends(get_db)):
    announcement = db.query(Announcements).filter(Announcements.id == announcement_id).first()
    if announcement is None:
        raise HTTPException(status_code=404, detail="Anunțul nu a fost găsit")

    images = db.query(Image).filter(Image.announcement_id == announcement_id).all()
    data = []
    for image in images:
        data.append({'id': image.id, 'image_url': f"{image.filename}"})
    return data


@router.delete("/delete/{image_id}")
async def delete_image(image_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    db_image = db.query(Image).filter(Image.id == image_id).first()

    if not db_image:
        raise HTTPException(status_code=404, detail="Imaginea nu a fost găsită")

    db_announcement = db.query(Announcements).filter(Announcements.id == db_image.announcement_id).first()
    image_user_id = db_announcement.user_id
    if current_user.get('id') != image_user_id:
        raise HTTPException(status_code=403,
                            detail="ID-ul utilizatorului nu corespunde cu ID-ul anunțului")

    # Delete the file from the filesystem
    image_path = os.path.join(UPLOAD_DIR, db_image.filename)
    if os.path.exists(image_path):
        os.remove(image_path)

    # Delete the image from the database
    db.delete(db_image)
    db.commit()

    return {"message": "Imaginea a fost ștearsă cu succes"}