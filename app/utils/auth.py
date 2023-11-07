from datetime import datetime, timedelta

from jose import jwt
from sqlalchemy.orm import Session

from app.crud import get_user_by_username
from app.utils.password import verify_password

from app.database import engine


def authenticate_user(username: str, password: str):
    with Session(engine) as session:
        user = get_user_by_username(session, username)
    if not user:
        return False
    if not verify_password(password, user.hashedPassword):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    from app.settings import ALGORITHM
    from app.settings import SECRET_KEY

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
