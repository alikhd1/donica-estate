from datetime import datetime

from sqlalchemy.orm import Session

from . import models, schemas


def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.userName == username).first()


def update_user(db: Session, user_id: int, user: schemas.UserUpdate) -> models.User:
    db_user: models.User = db.query(models.User).filter(models.User.id == user_id).first()

    for field, value in user.dict(exclude_unset=True).items():
        setattr(db_user, field, value)
    setattr(db_user, 'updatedAt', datetime.utcnow())

    db.commit()
    db.refresh(db_user)
    return db_user


def get_listing_by_id(db: Session, id: int) -> models.Listing:
    return db.query(models.Listing).filter(models.Listing.id == id).first()


def create_listing(db: Session, user_id: int, listing: schemas.ListingCreateUpdate) -> models.Listing:
    db_listing = models.Listing(**listing.dict())
    setattr(db_listing, 'user_id', user_id)

    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing


def update_listing(db: Session, db_listing: models.Listing, listing: schemas.ListingCreateUpdate) -> models.Listing:
    for field, value in listing.dict(exclude_unset=True).items():
        setattr(db_listing, field, value)
    setattr(db_listing, 'updatedAt', datetime.utcnow())

    db.commit()
    db.refresh(db_listing)
    return db_listing


def delete_listing(db: Session, db_listing: models.Listing):
    db.delete(db_listing)
    db.commit()
