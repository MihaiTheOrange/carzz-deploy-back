from typing import List
from uuid import uuid4
from fastapi import FastAPI
from models import Gender, Role, User

app = FastAPI()

db: List[User] = [
    User(id=uuid4(), first_name="Jamila", last_name="Ahmed", gender=Gender.female, roles=[Role.student]),
    User(id=uuid4(), first_name="Alex",last_name="Josenes",gender=Gender.male,roles=[Role.admin, Role.user])
]

@app.get("/")
async def root():
    return {"Hello": "Mondo"}

@app.get("/api/v1/users")
async def fetch_users():
    return db;