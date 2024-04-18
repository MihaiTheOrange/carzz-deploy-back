from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal

import crud
import schemas
import auth
from models import SellerRating

router = APIRouter(
    prefix='/ratings',
    tags=['ratings']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{seller_id}", response_model=schemas.SellerRating)
def create_rating(rating: schemas.SellerRatingCreate, db: Session = Depends(get_db),
                  current_user: dict = Depends(auth.get_current_user)):
    return crud.create_rating(db=db, rating=rating, user_id=current_user.get('id'))


@router.get('/seller_ratings/{seller_id}/', response_model=List[schemas.SellerRating])
def read_seller_ratings(seller_id: int, db: Session = Depends(get_db)):
    seller_ratings = crud.get_seller_ratings(db=db, seller_id=seller_id)
    if not seller_ratings:
        raise HTTPException(status_code=404, detail="Ratings not found")
    return seller_ratings


@router.get('/mywritenratings/', response_model=List[schemas.SellerRating])
def read_my_writen_ratings(user_id: int, db: Session = Depends(get_db)):
    ratings = crud.get_my_writen_ratings(db=db, user_id=user_id)
    if not ratings:
        raise HTTPException(status_code=404, detail="Ratings not found")
    return ratings


@router.get('/{rating_id}', response_model=schemas.SellerRating)
def read_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = crud.get_rating(db=db, rating_id=rating_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating


@router.put('/{rating_id}', response_model=schemas.SellerRating)
def update_rating(rating_id: int, rating_update: schemas.SellerRatingUpdate,
                  db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    db_rating = crud.get_rating(db=db, rating_id=rating_id)
    if not db_rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    if db_rating.user_id != current_user.get('id'):
        raise HTTPException(status_code=403, detail="You are not authorized to edit this rating")
    return crud.update_rating(db=db, rating=db_rating, rating_update=rating_update)