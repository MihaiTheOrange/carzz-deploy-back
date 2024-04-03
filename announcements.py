from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal

import crud
import schemas
import auth
from models import Announcements

router = APIRouter(
    prefix='/announcements',
    tags=['announcements']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Announcements
@router.post("/", response_model=schemas.Announcement)
def create_announcement(announcement: schemas.AnnouncementCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    return crud.create_announcement(db=db, announcement=announcement, user_id=current_user.get('id'))


# Get Announcements
@router.get("/", response_model=List[schemas.Announcement])
def read_announcements(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    announcements = crud.get_announcements(db=db, skip=skip, limit=limit)
    return announcements


# Get Announcements by ID
@router.get("/{announcement_id}", response_model=schemas.Announcement)
def read_announcement(announcement_id: int, db: Session = Depends(get_db)):
    db_announcement = crud.get_announcement(db=db, announcement_id=announcement_id)
    if db_announcement is None:
        raise HTTPException(status_code=404, detail="Announcements not found")
    return db_announcement

# Search Announcements
@router.get("/search/")
async def search_announcements(
    make: str = Query(None),
    model: str = Query(None),
    min_year: int = Query(None),
    max_year: int = Query(None),
    min_price: int = Query(None),
    max_price: int = Query(None),
    db: Session = Depends(get_db)
):
    # Build the base query
    query = db.query(Announcements)

    # Apply filters based on query parameters
    if make:
        query = query.filter(Announcements.make.ilike(f"%{make}%"))
    if model:
        query = query.filter(Announcements.model.ilike(f"%{model}%"))
    if min_year:
        query = query.filter(Announcements.year >= min_year)
    if max_year:
        query = query.filter(Announcements.year <= max_year)
    if min_price:
        query = query.filter(Announcements.price >= min_price)
    if max_price:
        query = query.filter(Announcements.price <= max_price)

    # Execute the query and return results
    announcements = query.all()
    return announcements


# Update Announcements
@router.put("/{announcement_id}", response_model=schemas.Announcement)
def update_announcement(announcement_id: int, announcement_update: schemas.AnnouncementUpdate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    db_announcement = crud.get_announcement(db=db, announcement_id=announcement_id)
    if db_announcement is None:
        raise HTTPException(status_code=404, detail="Announcements not found")
    if db_announcement.user_id != current_user.get('id'):
        raise HTTPException(status_code=403, detail="You are not allowed to update this announcement")
    return crud.update_announcement(db=db, announcement=db_announcement, announcement_update=announcement_update)


# Delete Announcements
@router.delete("/{announcement_id}")
def delete_announcement(announcement_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    db_announcement = crud.get_announcement(db=db, announcement_id=announcement_id)
    if db_announcement is None:
        raise HTTPException(status_code=404, detail="Announcements not found")
    if db_announcement.user_id != current_user.get('id'):
        raise HTTPException(status_code=403, detail="You are not allowed to delete this announcement")
    crud.delete_announcement(db=db, announcement_id=announcement_id)
    return {"message": "Announcements deleted successfully"}
