from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import auth
import schemas
from database import SessionLocal
from models import Announcements, Favorite
from typing import List

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


def check_favorite(user_id: int, announcement_id: int, dbb: Session = Depends(get_db)):
    favorite = dbb.query(Favorite).filter(Favorite.user_id == user_id, Favorite.announcement_id == announcement_id).first()
    return favorite is not None



@router.post('/addfavorite')
def add_favorite(favorite: schemas.Favorite, db: Session = Depends(get_db),current_user: dict = Depends(auth.get_current_user)):
    if db.query(Favorite).filter(Favorite.user_id == current_user.get('id')).count() >= 2:
        raise HTTPException(status_code=400, detail="Ai atins limita maximă de anunțuri favorite!")
    announcement = db.query(Announcements).filter(Announcements.id == favorite.announcement_id).first()
    if announcement is None:
        raise HTTPException(status_code=404, detail="Produsul nu a fost găsit!")
    if check_favorite(announcement_id = favorite.announcement_id, user_id=current_user.get('id'), dbb=db):
        raise HTTPException(status_code=409, detail="Produsul este deja salvat la favorite!")
    return crud.add_favorite(db, favorite, id=current_user.get('id'))



@router.get('/readfavorites',response_model=List[schemas.Announcement])
def get_favorites(db: Session = Depends(get_db),current_user: dict = Depends(auth.get_current_user)):
    current_id = current_user.get('id')
    return crud.read_favorites(db, current_id)



@router.delete('/delete/{announcement_id}')
def delete_favorite(announcement_id: int, db: Session = Depends(get_db),current_user: dict = Depends(auth.get_current_user)):
    user_id = current_user.get('id')
    db_favorite = crud.get_favorite(db, user_id, announcement_id)
    if db_favorite is None:
        raise HTTPException(status_code=404, detail="Anunțul favorit nu a fost găsit")
    crud.delete_favorite(db, announcement_id, user_id)
    return {"message": "Anunțul a fost șters de la favorite"}
