from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    full_name = Column(String, unique=True)
    email = Column(String, unique=True)
    role = Column(String)


class Cars(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    make = Column(String)
    model = Column(String)
    year = Column(Integer)
    mileage = Column(Float)
    price = Column(Float)
    additional_features = Column(String, nullable=True)

    # Establishing relationship with the Users table
    user = relationship("Users", back_populates="cars")
    announcements = relationship("Announcements", back_populates="car")


class Announcements(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    car_id = Column(Integer, ForeignKey('cars.id'))

    user = relationship("Users", back_populates="announcements")
    car = relationship("Cars", back_populates="announcements")

    @property
    def price(self):
        return self.car.price
