from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "d915b85bf3e4b2fdc3969a866cf24e721e2bc87f9ac6c5518e4f149c9de1b51f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
