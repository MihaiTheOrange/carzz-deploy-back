from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    full_name: str
    email: str
    role: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
