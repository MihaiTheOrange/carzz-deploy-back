from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import auth
import schemas
from database import SessionLocal
from models import Announcements,Favorite


router = APIRouter(
    prefix='/favorites',
    tags=['favorites']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_favorite(user_id: int, product_id: int, dbb: Session = Depends(get_db)):
    favorite = dbb.query(Favorite).filter(Favorite.user_id == user_id, Favorite.announcement_id == product_id).first()
    return favorite is not None
@router.post('/')
def add_favorite(favorite: schemas.Favorite, db: Session = Depends(get_db),current_user: dict = Depends(auth.get_current_user)):
    product = db.query(Announcements).filter(Announcements.id == favorite.announcement_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if check_favorite(product_id=favorite.announcement_id, user_id=current_user.get('id'), dbb=db):
        raise HTTPException(status_code=409, detail="Product already in favorites")
    return crud.add_favorite(db, favorite,id=current_user.get('id'))