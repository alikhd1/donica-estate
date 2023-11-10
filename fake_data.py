from sqlalchemy.ext.asyncio import AsyncSession
from app import models
from app import schemas
from sqlalchemy.future import select
from datetime import datetime

from app.database import engine


async def insert_fake_data():
    async with AsyncSession(engine) as session:
        existing_users = await session.execute(select(models.User).limit(1))
        user_exists = bool(existing_users.fetchone())

        if not user_exists:
            fake_users = [
                models.User(**schemas.UserUpdate(
                    userName="ali",
                    fullName="ali khandi",
                    email="alikhandi@gmail.com",
                    hashedPassword="Alik@1234",
                    DoB=datetime.utcnow(),
                    gender=schemas.Gender.Male,
                ).dict()),
                models.User(**schemas.UserUpdate(
                    userName="fatemeh",
                    fullName="fatemeh ahmadi ",
                    email="fatemeh@gmail.com",
                    hashedPassword="Fatemeh@1234",
                    DoB=datetime.utcnow(),
                    gender=schemas.Gender.Female,
                ).dict()),
                models.User(**schemas.UserUpdate(
                    userName="mohammad",
                    fullName="mohammad mohammadi ",
                    email="mohammad@gmail.com",
                    hashedPassword="Mohammad@1234",
                    DoB=datetime.utcnow(),
                    gender=schemas.Gender.Male,
                ).dict())

            ]
            session.add_all(fake_users)
            await session.commit()


if __name__ == "__main__":
    import asyncio

    asyncio.run(insert_fake_data())
