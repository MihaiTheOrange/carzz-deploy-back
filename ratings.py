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


@router.post("/", response_model=schemas.SellerRating)
def create_rating(rating: schemas.SellerRatingCreate, db: Session = Depends(get_db),
                  current_user: dict = Depends(auth.get_current_user)):
    return crud.create_rating(db=db, rating=rating, user_id=current_user.get('id'))


@router.get('/seller_ratings/{seller_id}/', response_model=schemas.SellerRating)
def read_seller_ratings(seller_id: int, db: Session = Depends(get_db)):
    seller_ratings = crud.get_seller_ratings(db=db, seller_id=seller_id)
    if not seller_ratings:
        raise HTTPException(status_code=404, detail="Ratings not found")
    return seller_ratings


@router.get('/myratings/', response_model=schemas.SellerRating)
def read_my_writen_ratings(user_id: int, db: Session = Depends(get_db)):
    ratings = crud.get_my_writen_ratings(db=db, user_id=user_id)
    if not ratings:
        raise HTTPException(status_code=404, detail="Ratings not found")
    return ratings

'''
@router.put('/{rating_id}', response_model=schemas.SellerRating)
def update_rating(rating_id: int, rating_)'''