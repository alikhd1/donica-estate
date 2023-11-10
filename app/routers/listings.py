from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session
from starlette import status

from app import schemas, models
from app.crud import get_listing_by_id, create_listing, update_listing, delete_listing
from app.database import get_session, engine
from app.models import Listing
from app.schemas import User
from app.utils.user import get_current_active_user

router = APIRouter()


@router.get("/{listing_id}", response_model=schemas.ReadListing)
async def read_listing(listing_id: int, db: Session = Depends(get_session)):
    """
    Retrieve details of a listing by its ID.

    ### Path Parameters
    - `listing_id`: ID of the listing.

    ### Response Model
    - `ReadListing`: Details of the listing.

    ### Dependencies
    - `get_db`: Dependency to get the database session.

    ### Tags
    - `Listing`: Endpoints related to listing operations.
    """
    async with AsyncSession(engine) as session:
        listing = await get_listing_by_id(session, listing_id)
        if not listing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")
    return listing


@router.post("/", response_model=schemas.Listing)
async def create_listing_(current_user: Annotated[User, Depends(get_current_active_user)],
                          listing: schemas.ListingCreateUpdate,
                          db: Session = Depends(get_session)):
    """
    Create a new listing.

    ### Request Body
    - `listing`: Details of the listing to be created.

    ### Response Model
    - `Listing`: Details of the created listing.

    ### Dependencies
    - `get_current_active_user`: Dependency to get the currently authenticated user.
    - `get_db`: Dependency to get the database session.

    ### Tags
    - `Listing`: Endpoints related to listing operations.
    """
    async with AsyncSession(engine) as session:
        db_listing = await create_listing(session, current_user.id, listing)
    return db_listing


@router.put("/{listing_id}/", response_model=schemas.Listing)
async def update_listing_(
        current_user: Annotated[User, Depends(get_current_active_user)],
        listing_id: int,
        listing_update: schemas.ListingCreateUpdate,
        db: Session = Depends(get_session)):
    """
    Update a listing by its ID.

    ### Path Parameters
    - `listing_id`: ID of the listing.

    ### Request Body
    - `listing_update`: Details to update in the listing.

    ### Response Model
    - `Listing`: Updated details of the listing.

    ### Dependencies
    - `get_current_active_user`: Dependency to get the currently authenticated user.
    - `get_db`: Dependency to get the database session.

    ### Tags
    - `Listing`: Endpoints related to listing operations.
    """
    async with AsyncSession(engine) as session:
        db_listing: Listing = await get_listing_by_id(session, listing_id)

        if not db_listing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")

        if not db_listing.user_id == current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner can edit")

        db_listing = await update_listing(session, db_listing, listing_update)

    return db_listing


@router.delete("/{listing_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_listing_(
        current_user: Annotated[User, Depends(get_current_active_user)],
        listing_id: int,
        db: Session = Depends(get_session)):
    """
    Delete a listing by its ID.

    ### Path Parameters
    - `listing_id`: ID of the listing.

    ### Response Model
    - No content (HTTP 204).

    ### Dependencies
    - `get_current_active_user`: Dependency to get the currently authenticated user.
    - `get_db`: Dependency to get the database session.

    ### Tags
    - `Listing`: Endpoints related to listing operations.
    """
    async with AsyncSession(engine) as session:
        db_listing: Listing = await get_listing_by_id(session, listing_id)

        if not db_listing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")

        if not db_listing.user_id == current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner can delete")

        await delete_listing(session, db_listing)
    return {}
