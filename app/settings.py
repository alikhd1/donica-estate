import os
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "d915b85bf3e4b2fdc3969a866cf24e721e2bc87f9ac6c5518e4f149c9de1b51f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_USER = os.getenv("POSTGRES_USER", "dornica")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "very_hard_to_guess")
POSTGRES_DB = os.getenv("POSTGRES_DB", "dornica")
