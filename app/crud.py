from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from . import models, schemas

from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_by_username(db: AsyncSession, username: str) -> models.User:
    statement = select(models.User).filter(models.User.userName == username)
    result = await db.execute(statement)
    return result.scalars().first()


async def update_user(db: AsyncSession, user_id: int, user: schemas.UserCreate) -> models.User:
    statement = select(models.User).filter(models.User.id == user_id)
    result = await db.execute(statement)
    db_user = result.scalars().first()

    for field, value in user.dict(exclude_unset=True).items():
        setattr(db_user, field, value)
    setattr(db_user, 'updatedAt', datetime.utcnow())

    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_listing_by_id(db: AsyncSession, id: int) -> models.Listing:
    statement = select(models.Listing).filter(models.Listing.id == id)
    result = await db.execute(statement)
    return result.scalars().first()


async def create_listing(db: AsyncSession, user_id: int, listing: schemas.ListingCreate) -> models.Listing:
    db_listing = models.Listing(**listing.dict())
    setattr(db_listing, 'user_id', user_id)

    db.add(db_listing)
    await db.commit()
    await db.refresh(db_listing)
    return db_listing


async def update_listing(db: AsyncSession, db_listing: models.Listing, listing: schemas.ListingUpdate) -> models.Listing:
    for field, value in listing.dict(exclude_unset=True).items():
        setattr(db_listing, field, value)
    setattr(db_listing, 'updatedAt', datetime.utcnow())

    await db.commit()
    await db.refresh(db_listing)
    return db_listing


async def delete_listing(db: AsyncSession, db_listing: models.Listing):
    await db.delete(db_listing)
    await db.commit()