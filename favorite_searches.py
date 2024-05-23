from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal

import crud
import schemas
import auth
from models import FavoriteSearches


router = APIRouter(
    prefix='/favorite-searches',
    tags=['favorite-searches'],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add/", response_model=schemas.FavoriteSearchResponse)
async def create_favorite_search(
    search: schemas.FavoriteSearchCreate,
    current_user: dict = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    favorite_search = FavoriteSearches(
        user_id=current_user.get('id'),
        make=search.make,
        model=search.model,
        min_year=search.min_year,
        max_year=search.max_year,
        min_mileage=search.min_mileage,
        max_mileage=search.max_mileage,
        min_cylinder_volume=search.min_cylinder_volume,
        max_cylinder_volume=search.max_cylinder_volume,
        min_price=search.min_price,
        max_price=search.max_price,
        fuel_type=search.fuel_type,
        gearbox=search.gearbox,
        car_body=search.car_body,
        seats=search.seats,
        min_horsepower=search.min_horsepower,
        max_horsepower=search.max_horsepower,
        color=search.color,
        created_at=datetime.utcnow()
    )
    db.add(favorite_search)
    db.commit()
    db.refresh(favorite_search)
    return favorite_search


@router.get("/get_favorite_searches/", response_model=List[schemas.FavoriteSearchResponse])
async def get_favorite_searches(current_user: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    favorite_searches = db.query(FavoriteSearches).filter(FavoriteSearches.user_id == current_user.get('id')).all()
    return favorite_searches

@router.get("/get_by_id/{search_id}", response_model=schemas.FavoriteSearchResponse)
async def get_favorite_search(search_id: int, db: Session = Depends(get_db)):
    favorite_search = db.query(FavoriteSearches).filter(FavoriteSearches.id == search_id).first()
    if not favorite_search:
        raise HTTPException(status_code=404, detail="Favorite search not found")
    return favorite_search


@router.delete("/delete/{search_id}", status_code=204)
async def delete_favorite_search(search_id: int, db: Session = Depends(get_db)):
    favorite_search = db.query(FavoriteSearches).filter(FavoriteSearches.id == search_id).first()
    if not favorite_search:
        raise HTTPException(status_code=404, detail="Favorite search not found")

    db.delete(favorite_search)
    db.commit()
    return