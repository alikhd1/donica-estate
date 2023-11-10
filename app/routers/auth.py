from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.requests import Request

from app.schemas import Token
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.auth import authenticate_user, create_access_token
from app.utils.redis import get_user_jwt_token, add_to_blacklist, set_user_token
from app.utils.throttle import limiter

from fastapi import APIRouter

router = APIRouter()


@router.post("/token", response_model=Token)
@limiter.limit("5/minute")
async def login_for_access_token(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.userName}, expires_delta=access_token_expires
    )
    jwt_token = await get_user_jwt_token(user.id)
    if jwt_token:
        await add_to_blacklist(jwt_token)
    await set_user_token(user.id, access_token)
    print(f'user logged in: {user.userName}')
    return {"access_token": access_token, "token_type": "bearer"}
