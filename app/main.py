import logging

from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .database import Base, engine
from .routers import users, listings, auth
from .utils.log import logging_config
from .utils.middleware import RouterLoggingMiddleware
from .utils.throttle import limiter


def create_db_and_tables():
    Base.metadata.create_all(engine)


app = FastAPI()

# app.add_middleware(
#     RouterLoggingMiddleware,
#     logger=logging.getLogger(__name__)
# )

# logging.config.dictConfig(logging_config)

app.limiter = limiter
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


app.include_router(auth.router, tags=['Auth'])
app.include_router(users.router, prefix='/users', tags=['Users'])
app.include_router(listings.router, prefix='/listing', tags=['Listings'])
