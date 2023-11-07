import logging
from datetime import timedelta
from typing import Annotated

from app import schemas, models
from app.crud import get_listing_by_id, update_user, create_listing, update_listing, delete_listing
from app.models import Listing
from app.schemas import Token, User
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.auth import authenticate_user, create_access_token

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from sqlmodel import Session

from app.database import engine, Base, get_db
from app.utils.log import logging_config
from app.utils.redis import set_user_token, get_user_jwt_token, add_to_blacklist
from app.utils.user import get_current_active_user


logging.config.dictConfig(logging_config)


def create_db_and_tables():
    Base.metadata.create_all(engine)


limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.on_event("startup")
async def update_counter():
    with open("count.txt", "r") as file:
        current_counter = int(file.read().strip())

    updated_counter = current_counter + 1

    with open("count.txt", "w") as file:
        file.write(str(updated_counter))


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# @app.get("/")
async def root():
    return {"message": "hello World"}


@app.post("/token", response_model=Token)
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


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@app.put("/users/me/", response_model=User)
async def update_profile(current_user: Annotated[User, Depends(get_current_active_user)],
                         user: schemas.UserUpdate,
                         db: Session = Depends(get_db)):
    with db as session:
        user = update_user(session, current_user.id, user)
    return user


@app.get("/listing/{listing_id}", response_model=schemas.Listing)
async def read_listing(listing_id: int, db: Session = Depends(get_db)):
    with db as session:
        listing = get_listing_by_id(session, listing_id)
    return listing


@app.post("/listing/", response_model=schemas.Listing)
async def create_listing_(current_user: Annotated[User, Depends(get_current_active_user)],
                          listing: schemas.ListingCreateUpdate,
                          db: Session = Depends(get_db)):
    with db as session:
        db_listing = create_listing(session, current_user.id, listing)
    return db_listing


@app.put("/listing/{listing_id}/", response_model=schemas.Listing)
async def update_listing_(
        current_user: Annotated[User, Depends(get_current_active_user)],
        listing_id: int,
        listing_update: schemas.ListingCreateUpdate,
        db: Session = Depends(get_db)):
    with db as session:
        db_listing: Listing = get_listing_by_id(session, listing_id)

        if not db_listing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")

        if not db_listing.user_id == current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner can edit")

        db_listing = update_listing(session, db_listing, listing_update)

    return db_listing


@app.delete("/listing/{listing_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_listing_(
        current_user: Annotated[User, Depends(get_current_active_user)],
        listing_id: int,
        db: Session = Depends(get_db)):
    with db as session:
        db_listing: Listing = session.query(models.Listing).filter(models.Listing.id == listing_id).first()

        if not db_listing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")

        if not db_listing.user_id == current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner can delete")

        delete_listing(session, db_listing)
    return {}
