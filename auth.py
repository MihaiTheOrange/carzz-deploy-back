from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from schemas import CreateUserRequest, Token
import logging
from fastapi import Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = 'yc{qq$f0#6uLOLbUfuT<S==*<z@$/Harp&O1a*m+mSnc#iKp.}=$Re!hU`+H"|='
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# Endpoint for creating a new user
@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest,
                      request: Request):
    try:
        user_db = db.query(Users).filter(create_user_request.username == Users.username).first()
        if user_db:
            raise HTTPException(status_code=400, detail="Numele de utilizator este deja folosit")

        user_db_email = db.query(Users).filter(create_user_request.email == Users.email).first()
        if user_db_email:
            raise HTTPException(status_code=400, detail="Emailul introdus este deja asociat unui cont existent")

        user_db_phone = db.query(Users).filter(create_user_request.phone_number == Users.phone_number).first()
        if user_db_phone:
            raise HTTPException(status_code=400, detail="Numărul de telefon introdus este deja asociat unui cont existent")

        create_user_model = Users(
            username=create_user_request.username,
            hashed_password=bcrypt_context.hash(create_user_request.password),
            full_name=create_user_request.full_name,
            email=create_user_request.email,
            county=create_user_request.county,
            phone_number=create_user_request.phone_number,
        )

        db.add(create_user_model)
        db.commit()
        return {"message": f"Utilizatorul {create_user_request.username} este creat!"}

    except HTTPException as e:
        logger.error(f"HTTP Exception: {e.detail}")
        raise e
    except Exception as e:
        request_body = await request.json()
        logger.error(f"Validation Error: {str(e)}")
        logger.error(f"Request Body: {request_body}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Validation error occurred. Check the logs for more details.")


# Endpoint for login
@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Utilizatorul nu a putut fi validat')
    token = create_access_token(user.username, user.id, timedelta(minutes=100))

    return {'access_token': token, 'token_type': 'bearer'}


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return None
    if not bcrypt_context.verify(password, user.hashed_password):
        return None
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Utilizatorul nu a putut fi validat')
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Utilizatorul nu a putut fi validat')
