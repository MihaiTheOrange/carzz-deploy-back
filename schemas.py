from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    username: str
    password: str
    full_name: str
    email: str
    role: str

    class Config:
        from_attributes = True


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


class Car(BaseModel):
    make: str
    model: str
    year: int
    mileage: float
    price: float
    additional_features: str = None

    class Config:
        from_attributes = True
