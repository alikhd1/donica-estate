from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    userName = Column(String)
    fullName = Column(String)
    email = Column(String)
    hashedPassword = Column(String)
    DoB = Column(DateTime)
    gender = Column(String)
    createdAt = Column(DateTime, default=lambda: datetime.utcnow())
    updatedAt = Column(DateTime, default=lambda: datetime.utcnow())

    listings = relationship("Listing", back_populates="user")


class Listing(Base):
    __tablename__ = "listing"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    availableNow = Column(Boolean)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="listings")
    address = Column(String)
    createdAt = Column(DateTime, default=lambda: datetime.utcnow())
    updatedAt = Column(DateTime, default=lambda: datetime.utcnow())
