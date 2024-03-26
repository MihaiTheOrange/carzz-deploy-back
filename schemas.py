from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    username: str
    password: str
    full_name: str
    email: str
    role: str


class UserUpdate(BaseModel):
    username: str
    password: str
    full_name: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    id: int

    class Config:
        from_attributes = True



