from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import SessionLocal
from models import ProfilePic
from models import Users

import os
import shutil
import auth
import uuid
from SupaB import supabase, BUCKET_PROF_PIC


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


# @router.put("/upload/")
# async def upload_image(uploaded_file: UploadFile = File(...), db: Session = Depends(get_db),
#                        current_user: dict = Depends(auth.get_current_user)):
#     db_pic = db.query(ProfilePic).filter(ProfilePic.user_id == current_user.get('id')).first()
#
#     # Generate a unique name for the file
#     unique_filename = str(uuid.uuid4()) + os.path.splitext(uploaded_file.filename)[1]
#
#     if db_pic:
#         image_path = os.path.join(UPLOAD_DIR, db_pic.filename)
#         if os.path.exists(image_path):
#             os.remove(image_path)
#
#         with open(os.path.join(UPLOAD_DIR, unique_filename), "wb") as buffer:
#             shutil.copyfileobj(uploaded_file.file, buffer)
#
#         db_pic.filename = unique_filename
#         db.commit()
#     else:
#         with open(os.path.join(UPLOAD_DIR, unique_filename), "wb") as buffer:
#             shutil.copyfileobj(uploaded_file.file, buffer)
#
#         db_image = ProfilePic(filename=unique_filename)
#         db_image.user_id = current_user.get('id')
#         db.add(db_image)
#         db.commit()
#     return {"message": "Imaginea a fost încărcată cu succes"}


@router.put("/upload/")
async def upload_image(uploaded_file: UploadFile = File(...), db: Session = Depends(get_db),
                       current_user: dict = Depends(auth.get_current_user)):
    db_pic = db.query(ProfilePic).filter(ProfilePic.user_id == current_user.get('id')).first()

    # Generate a unique name for the file
    unique_filename = str(uuid.uuid4()) + os.path.splitext(uploaded_file.filename)[1]

    # Read file contents
    file_content = await uploaded_file.read()

    if db_pic:
        # If there is an existing profile picture, delete it from the Supabase bucket
        supabase.storage.from_(BUCKET_PROF_PIC).remove([db_pic.filename])

        # Upload the new file to Supabase
        response = supabase.storage.from_(BUCKET_PROF_PIC).upload(unique_filename, file_content)

        # Check for successful upload
        if not response.path:
            raise HTTPException(status_code=500, detail="Failed to upload image to Supabase storage")
        image_url = supabase.storage.from_(BUCKET_PROF_PIC).get_public_url(response.path)
        # Update the filename in the database
        db_pic.filename = image_url
        print(response.path)
        db.commit()
    else:
        # Upload new file to Supabase
        response = supabase.storage.from_(BUCKET_PROF_PIC).upload(unique_filename, file_content)

        # Check for successful upload
        if not response.path:
            raise HTTPException(status_code=500, detail="Failed to upload image to Supabase storage")

        # Add a new profile picture record in the database
        image_url = supabase.storage.from_(BUCKET_PROF_PIC).get_public_url(response.path)
        db_image = ProfilePic(filename=image_url, user_id=current_user.get('id'))
        db.add(db_image)
        db.commit()

    return {"message": "Imaginea a fost încărcată cu succes"}


@router.get("/get/{user_id}")
async def get_pfp(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Utilizatorul nu a fost găsit")

    pfp = db.query(ProfilePic).filter(ProfilePic.user_id == user_id).first()
    if pfp is None:
        image_url = ""
    else:
        image_url = pfp.filename
    return {"image_urls": image_url}


