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
@router.post("/create")
def create_announcement(announcement: schemas.AnnouncementCreate, db: Session = Depends(get_db),
                        current_user: dict = Depends(auth.get_current_user)):
    crud.create_announcement(db=db, announcement=announcement, user_id=current_user.get('id'))
    return {"message": "Anunțul a fost creat"}


# Get all Announcements
@router.get("/getall", response_model=List[schemas.Announcement])
def read_announcements(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    announcements = crud.get_announcements(db=db, skip=skip, limit=limit)
    return announcements


# Get Announcements by ID
@router.get("/idget/{announcement_id}", response_model=schemas.Announcement)
def read_announcement(announcement_id: int, db: Session = Depends(get_db)):
    db_announcement = crud.get_announcement(db=db, announcement_id=announcement_id)
    if db_announcement is None:
        raise HTTPException(status_code=404, detail="Anunțul nu a fost găsit")
    return db_announcement


# Get my announcements
@router.get("/my_announcements/", response_model=List[schemas.Announcement])
def get_my_announcements(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    announcements = crud.get_my_announcements(db=db, user_id=current_user.get('id'))
    if announcements is None:
        raise HTTPException(status_code=404, detail="Anunțul nu a fost găsit")
    return announcements


# Search Announcements
@router.get("/search/")
async def search_announcements(
        make: str = Query(None),
        model: str = Query(None),
        min_year: int = Query(None),
        max_year: int = Query(None),
        min_mileage: int = Query(None),
        max_mileage: int = Query(None),
        min_cylinder_volume: int = Query(None),
        max_cylinder_volume: int = Query(None),
        min_price: int = Query(None),
        max_price: int = Query(None),
        fuel_type: str = Query(None),
        gearbox: str = Query(None),
        car_body: str = Query(None),
        seats: str = Query(None),
        min_horsepower: str = Query(None),
        max_horsepower: str = Query(None),
        color: str = Query(None),
        db: Session = Depends(get_db)
):
    # Build the base query
    query = db.query(Announcements)

    # Apply filters based on query parameters
    if make:
        query = query.filter(Announcements.make.ilike(f"%{make}%"))
    if model:
        query = query.filter(Announcements.model.ilike(f"%{model}%"))
    if min_mileage:
        query = query.filter(Announcements.mileage >= min_mileage)
    if max_mileage:
        query = query.filter(Announcements.mileage <= max_mileage)
    if min_cylinder_volume:
        query = query.filter(Announcements.motor_capacity >= min_cylinder_volume)
    if max_cylinder_volume:
        query = query.filter(Announcements.motor_capacity <= max_cylinder_volume)
    if fuel_type:
        query = query.filter(Announcements.fuel_type.ilike(f"%{fuel_type}%"))
    if gearbox:
        query = query.filter(Announcements.gearbox.ilike(f"%{gearbox}%"))
    if car_body:
        query = query.filter(Announcements.car_body.ilike(f"%{car_body}%"))
    if seats:
        query = query.filter(Announcements.seats.ilike(f"%{seats}%"))
    if min_horsepower:
        query = query.filter(Announcements.horsepower >= min_horsepower)
    if max_horsepower:
        query = query.filter(Announcements.horsepower >= max_horsepower)
    if color:
        query = query.filter(Announcements.color.ilike(f"%{color}%"))
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


@router.get('/raport/')
def get_link_raport(announcement_id: int, db: Session = Depends(get_db)):
    db_announcement = crud.get_announcement(db=db, announcement_id=announcement_id)
    return f'https://www.carvertical.com/ro/precheck?vin={db_announcement.VIN}'


# Update Announcements
@router.put("/update/{announcement_id}", response_model=schemas.Announcement)
def update_announcement(announcement_id: int, announcement_update: schemas.AnnouncementUpdate,
                        db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    db_announcement = crud.get_announcement(db=db, announcement_id=announcement_id)
    if db_announcement is None:
        raise HTTPException(status_code=404, detail="Anunțul nu a fost găsit")
    if db_announcement.user_id != current_user.get('id'):
        raise HTTPException(status_code=403, detail="Nu puteți actualiza acest anunț")
    return crud.update_announcement(db=db, announcement=db_announcement, announcement_update=announcement_update)


# Delete Announcements
@router.delete("/delete/{announcement_id}")
def delete_announcement(announcement_id: int, db: Session = Depends(get_db),
                        current_user: dict = Depends(auth.get_current_user)):
    db_announcement = crud.get_announcement(db=db, announcement_id=announcement_id)
    if db_announcement is None:
        raise HTTPException(status_code=404, detail="Anunțul nu a fost găsit")
    if db_announcement.user_id != current_user.get('id'):
        raise HTTPException(status_code=403, detail="Nu puteți actualiza acest anunț")
    crud.delete_announcement(db=db, announcement_id=announcement_id)
    return {"message": "Anunțul a fost șters cu succes"}
