from typing import List
from uuid import UUID
from fastapi import FastAPI
from models import Role, User

app = FastAPI()

db: List[User] = [
    User(id=UUID("eea55460-5d3c-4679-a78c-b53d764f6b35"),
         first_name="Jamila",
         last_name="Ahmed",
         roles=[Role.student]),
    User(id=UUID("eb55ddeb-efd6-41f8-a133-cf80a20c7a84"),
         first_name="Alex",
         last_name="Jones",
         roles=[Role.admin, Role.user])
]


@app.get("/")
async def root():
    return {"Hello": "Mondo"}


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}
