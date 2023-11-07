import secrets
import string
from datetime import datetime
from typing import Optional

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

    token = relationship("Token", uselist=False, back_populates="user")
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


class Token(Base):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    user = relationship("User", back_populates="token")

    def generate_token(self, token_length=32):
        token_characters = string.ascii_letters + string.digits
        self.token = ''.join(secrets.choice(token_characters) for _ in range(token_length))

    def __init__(self, *args, **kwargs):
        super(Token, self).__init__(*args, **kwargs)
        self.generate_token()
