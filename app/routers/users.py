from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app import schemas
from app.crud import update_user
from app.database import get_db

from app.schemas import User
from app.utils.user import get_current_active_user

router = APIRouter()


@router.get("/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    """
    Retrieve details of the currently authenticated user.

    ### Response Model
    - `User`: User details including username, full name, email, date of birth, and gender.

    ### Dependencies
    - `get_current_active_user`: Dependency to get the currently authenticated user.

    ### Tags
    - `User`: Endpoints related to user operations.
    """
    return current_user


@router.put("/me/", response_model=User)
async def update_profile(current_user: Annotated[User, Depends(get_current_active_user)],
                         user: schemas.UserUpdate,
                         db: Session = Depends(get_db)):
    """
    Update the profile of the currently authenticated user.

    ### Request Body
    - `user`: User update details including full name, email, date of birth, and gender.

    ### Response Model
    - `User`: Updated user details including username, full name, email, date of birth, and gender.

    ### Dependencies
    - `get_current_active_user`: Dependency to get the currently authenticated user.
    - `get_db`: Dependency to get the database session.

    ### Tags
    - `User`: Endpoints related to user operations.
    """
    with db as session:
        user = update_user(session, current_user.id, user)
    return user
