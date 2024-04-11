from sqlalchemy import Column, Integer, String, Float, ForeignKey, LargeBinary
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    full_name = Column(String)
    email = Column(String, unique=True)
    county = Column(String)

    announcements = relationship("Announcements", back_populates="user")


class Announcements(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    make = Column(String)
    model = Column(String)
    year = Column(Integer)
    mileage = Column(Float)
    price = Column(Float)
    additional_features = Column(String, nullable=True)
    motor_capacity = Column(Integer)
    fuel_type = Column(String)
    gearbox = Column(String)
    car_body = Column(String)
    seats = Column(Integer)
    horsepower = Column(Integer)
    color = Column(String)
    condition = Column(String)

    user = relationship("Users", back_populates="announcements")


class Make(Base):
    __tablename__ = "make"

    title = Column(String, primary_key=True, index=True)


class Model(Base):
    __tablename__ = "model"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    make_id = Column(String, ForeignKey('make.title'))


class Favorite(Base):
    __tablename__ = "favorites"

    id=Column(Integer, primary_key=True)
    user_id=Column(Integer,ForeignKey('users.id'))
    announcement_id=Column(Integer,ForeignKey('announcements.id'))


class Image(Base):
    __tablename__ = "announcement_images"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    announcement_id = Column(Integer,ForeignKey('announcements.id'))