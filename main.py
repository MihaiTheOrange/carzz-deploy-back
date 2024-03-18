from typing import List
from fastapi import FastAPI

from models import User

app = FastAPI()

db: List[User]

@app.get("/")
async def root():
    return {"Hello": "Mondo"}