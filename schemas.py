from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    full_name: str
    email: str
    role: str


class CreateUserRequest(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    full_name: Optional[str]
    role: Optional[str]


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class AnnouncementBase(BaseModel):
    title: str
    description: str
    brand: str
    model: str
    year: int
    mileage: float
    price: float
    additional_features: Optional[str] = None
    motor_capacity = int
    fuel_type = str
    gearbox = str
    car_body = str
    seats = int
    horsepower = int
    color = str
    condition = str

    class Config:
        from_attributes = True


class AnnouncementCreate(AnnouncementBase):
    pass


class AnnouncementUpdate(AnnouncementBase):
    pass


class Announcement(AnnouncementBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
