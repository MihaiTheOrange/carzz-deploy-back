from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal

import crud
import schemas
import auth
from models import SellerRating, Users

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


@router.post("/rate", response_model=schemas.SellerRating)
def create_rating(rating: schemas.SellerRatingCreate, db: Session = Depends(get_db),
                  current_user: dict = Depends(auth.get_current_user)):
    db_seller = db.query(Users).filter(Users.id == rating.seller_id).first()

    if db_seller is None:
        raise HTTPException(status_code=404, detail="Utilizator inexistent")

    if db_seller.id == current_user.get('id'):
        raise HTTPException(status_code=409, detail="Operațiune invalidă")

    db_rating = db.query(SellerRating).filter(SellerRating.seller_id == rating.seller_id, SellerRating.user_id == current_user.get('id')).first()
    if db_rating:
        raise HTTPException(status_code=409, detail="Ați scris o recenzie deja")

    return crud.create_rating(db=db, rating=rating, user_id=current_user.get('id'))


@router.get('/seller_ratings/{seller_id}/', response_model=List[schemas.SellerRating])
def read_seller_ratings(seller_id: int, db: Session = Depends(get_db)):
    seller_ratings = crud.get_seller_ratings(db=db, seller_id=seller_id)
    if seller_ratings is None:
        raise HTTPException(status_code=404, detail="Nicio recenzie")
    return seller_ratings


@router.get('/my_writen_ratings/', response_model=List[schemas.SellerRating])
def read_my_writen_ratings(db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    ratings = crud.get_my_writen_ratings(db=db, user_id=current_user['id'])
    if not ratings:
        raise HTTPException(status_code=404, detail="Nicio recenzie")
    return ratings


@router.get('/read/{rating_id}', response_model=schemas.SellerRating)
def read_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = crud.get_rating(db=db, rating_id=rating_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Recenzia nu a fost găsită")
    return rating


@router.get('/average_rating/{seller_id}')
def get_rating(seller_id: int, db: Session = Depends(get_db)):
    seller_ratings = crud.get_seller_ratings(db=db, seller_id=seller_id)
    medium_rating = 0
    if len(seller_ratings) != 0:
        for rating in seller_ratings:
            medium_rating += rating.rating
        medium_rating /= len(seller_ratings)
    return medium_rating


@router.put('/put/{rating_id}', response_model=schemas.SellerRating)
def update_rating(rating_id: int, rating_update: schemas.SellerRatingUpdate,
                  db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    db_rating = crud.get_rating(db=db, rating_id=rating_id)
    if not db_rating:
        raise HTTPException(status_code=404, detail="Recenzia nu a fost găsită")
    if db_rating.user_id != current_user.get('id'):
        raise HTTPException(status_code=403, detail="Nu puteți modifica această recenzie")
    return crud.update_rating(db=db, rating=db_rating, rating_update=rating_update)


@router.delete('/delete/{rating_id}')
def delete_rating(rating_id: int, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
    db_rating = crud.get_rating(db=db, rating_id=rating_id)
    if not db_rating:
        raise HTTPException(status_code=404, detail="Recenzia nu a fost găsită")
    if db_rating.user_id != current_user.get('id'):
        raise HTTPException(status_code=403, detail="Nu puteți șterge această recenzie")
    crud.delete_rating(db=db, rating_id=rating_id)
    return {"message": "Recenzia a fost ștearsă"}

