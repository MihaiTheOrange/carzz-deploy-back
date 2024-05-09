from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
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
    phone_number = Column(String)

    announcements = relationship("Announcements", back_populates="user")


class Announcements(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True)
    created_at = Column(String, nullable=False)
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
    VIN = Column(String)
    views = Column(Integer)
    favs = Column(Integer)

    user = relationship("Users", back_populates="announcements")


class Make(Base):
    __tablename__ = "make"

    title = Column(String, primary_key=True, index=True)


class Model(Base):
    __tablename__ = "model"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    make_id = Column(String)


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    announcement_id = Column(Integer, ForeignKey('announcements.id'))


class SellerRating(Base):
    __tablename__ = 'seller_ratings'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    seller_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(String, nullable=False)

    # Define relationships
    user = relationship("Users", foreign_keys=[user_id], primaryjoin="SellerRating.user_id == Users.id")
    seller = relationship("Users", foreign_keys=[seller_id], primaryjoin="SellerRating.seller_id == Users.id")

    def __repr__(self):
        return f"<SellerRating(id={self.id}, rating={self.rating}, user_id={self.user_id}, seller_id={self.seller_id}, created_at={self.created_at})>"


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    announcement_id = Column(Integer, ForeignKey('announcements.id'))


class ProfilePic(Base):
    __tablename__ = "profile_pictures"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
