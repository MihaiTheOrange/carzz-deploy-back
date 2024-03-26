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


class Announcements(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("Users", back_populates="announcements")
