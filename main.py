from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import favorites
import announcements
from auth import get_current_user
from database import SessionLocal, engine

import auth
import crud
import models
import schemas

# Create FastAPI app instance
app = FastAPI()
app.include_router(auth.router)
app.include_router(announcements.router)
app.include_router(favorites.router)

# Create the database tables
models.Base.metadata.create_all(bind=engine)


# Dependency to get the database session
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
    return {"Welcome!"}


# Endpoint to get a user by ID
@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Users not found")
    return db_user


# Update Users Endpoint
@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Users not found")
    if db_user.id != current_user["id"]:
        raise HTTPException(status_code=403, detail="You are not allowed to update this user")
    updated_user = crud.update_user(db=db, user=db_user, user_update=user_update)
    return updated_user


# Delete Users Endpoint
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    if user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this user")
    else:
        deleted = crud.delete_user(db=db, user_id=user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Users not found")
        return {"message": "Users deleted successfully"}
