from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database import engine
from app.schemas import TokenData, User
from app.crud import get_user_by_username
from app.settings import oauth2_scheme, SECRET_KEY, ALGORITHM
from app.utils.redis import is_in_blacklist


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    with Session(engine) as session:
        user = get_user_by_username(session, username=token_data.username)
    if user is None:
        raise credentials_exception
    if await is_in_blacklist(token):
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

