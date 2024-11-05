from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
import favorites
import announcements
import ratings
from auth import get_current_user
from database import SessionLocal, engine

import user_profile_picture
import auth
import crud
import models
import schemas
import announcement_images
import favorite_searches
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app instance
app = FastAPI()
app.include_router(auth.router)
app.include_router(announcements.router)
app.include_router(favorites.router)
app.include_router(ratings.router)
app.include_router(announcement_images.router)
app.include_router(user_profile_picture.router)
app.include_router(favorite_searches.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create the database tables
models.Base.metadata.create_all(bind=engine)

app.mount("/uploads", StaticFiles(directory=announcement_images.UPLOAD_DIR), name="uploads")
app.mount("/profile_pictures", StaticFiles(directory=user_profile_picture.UPLOAD_DIR), name="profile_pictures")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@app.get("/")
def welcome():
    return {"Well!"}


# Endpoint to get a user by ID
@app.get("/users/read/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilizatorii nu au fost găsiți")
    return db_user


@app.get("/get/user/curent", response_model=schemas.User)
async def read_curent_user(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    user_id = current_user.get('id')
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilizatorii nu au fost găsiți")
    return db_user


# Update Users Endpoint
@app.put("/users/put", response_model=schemas.User)
def update_user(user_update: schemas.UserUpdate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    user_id = current_user.get("id")
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilizatorii nu au fost găsiți")
    if db_user.id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Nu puteți actualiza acest utilizator")
    updated_user = crud.update_user(db=db, user=db_user, user_update=user_update)
    return updated_user


@app.patch("/users/theme", response_model=schemas.User)
def update_user_theme(theme: schemas.UserThemeUpdate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    user_id = current_user.get("id")
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilizatorii nu au fost găsiți")
    if db_user.id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Nu puteți actualiza acest utilizator")
    updated_user_theme = crud.update_user_theme(db=db, user=db_user, theme=theme)
    return updated_user_theme


# Delete Users Endpoint
@app.delete("/users/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    if user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Nu puteți șterge acest utilizator")
    else:
        deleted = crud.delete_user(db=db, user_id=user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Utilizatorul nu a fost găsit")
        return {"message": "Utilizatorul a fost șters"}

