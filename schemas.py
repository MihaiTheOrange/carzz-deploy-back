from pydantic import BaseModel, Field
from typing import Optional
from pydantic import EmailStr


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    full_name: str = Field(min_length=3, max_length=30)
    email: EmailStr
    county: str = Field(min_length=3, max_length=30)
    phone_number: str = Field(min_length=5, max_length=15)


class CreateUserRequest(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    full_name: Optional[str]
    county: Optional[str]


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
    make: str
    model: str
    year: int
    mileage: float
    price: float
    additional_features: Optional[str] = None
    motor_capacity: int
    fuel_type: str
    gearbox: str
    car_body: str
    seats: int
    horsepower: int
    color: str
    condition: str

    class Config:
        from_attributes = True


class AnnouncementCreate(AnnouncementBase):
    pass


class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    mileage: Optional[float] = None
    price: Optional[float] = None
    additional_features: Optional[str] = None
    motor_capacity: Optional[int] = None
    fuel_type: Optional[str] = None
    gearbox: Optional[str] = None
    car_body: Optional[str] = None
    seats: Optional[int] = None
    horsepower: Optional[int] = None
    color: Optional[str] = None
    condition: Optional[str] = None


class Announcement(AnnouncementBase):
    id: int
    user_id: int
    user_phone_number: str

    class Config:
        from_attributes = True


class MyAnnouncement(Announcement):
    views: int


class Favorite(BaseModel):
    announcement_id: int


class SellerRatingBase(BaseModel):
    seller_id: int
    rating: int
    comment: Optional[str]


class SellerRatingCreate(SellerRatingBase):
    pass


class SellerRatingUpdate(BaseModel):
    rating: int
    comment: Optional[str]


class SellerRating(SellerRatingBase):
    id: int
    user_id: int
    created_at: str

    class Config:
        from_attributes = True
