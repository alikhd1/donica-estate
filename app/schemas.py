import re
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, validator

from app.utils.password import get_password_hash


class Gender(str, Enum):
    Male = "MALE"
    Female = "FEMALE"
    Not_Specified = "NOT_SPECIFIED"


class Type(str, Enum):
    House = "HOUSE"
    Apartment = "APARTMENT"


class User(BaseModel):
    id: int
    userName: str
    fullName: str | None = None
    email: EmailStr
    DoB: datetime
    gender: Gender = Field(default=Gender.Not_Specified)
    createdAt: datetime = Field(default_factory=lambda: datetime.now())
    updatedAt: datetime

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    userName: str
    fullName: str | None = None
    email: EmailStr
    DoB: datetime | None
    gender: Gender
    hashedPassword: str

    @validator('DoB')
    def year_is_after_1940(cls, value: datetime):
        if value.year < 1940:
            raise ValueError('year must be after 1940')
        return value

    @validator('hashedPassword')
    def validate_password(cls, value):
        rules = ('1. At least 8 characters long. '
                 '2. Contains at least one uppercase letter. '
                 '3. Contains at least one lowercase letter. '
                 '4. Contains at least one digit (number). '
                 '5. Contains at least one special character. '
                 )
        if (
                len(value) >= 8 and
                any(char.isupper() for char in value) and
                any(char.islower() for char in value) and
                any(char.isdigit() for char in value) and
                re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]', value)
        ):
            return get_password_hash(value)
        raise ValueError(f'your password must have these rules: {rules}')


class Listing(BaseModel):
    id: int
    type: Type
    availableNow: bool
    user_id: int
    address: str
    createdAt: datetime
    updatedAt: datetime | None

    class Config:
        orm_mode = True


class ListingCreateUpdate(BaseModel):
    type: Type
    availableNow: bool
    address: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class CounterModel(BaseModel):
    counter: int
