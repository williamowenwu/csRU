from datetime import datetime
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from .schemas import TokenData
from .config import settings
# SECRET KEY
# Algorithm
# Expiration time

ouath2_scheme = OAuth2PasswordBearer(tokenUrl=('/login'))
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_SECONDS = settings.access_token_expire_seconds


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = int(datetime.utcnow().timestamp()) + ACCESS_TOKEN_EXPIRE_SECONDS
    to_encode.update({"expire": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str, creds_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")
        expire = payload.get("expire")
        now = int(datetime.utcnow().timestamp())
        if not id:
            raise creds_exception

        if now > expire:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Please Revalidate Token")

        token_data = TokenData(id=id)
    except JWTError:
        raise creds_exception
    return token_data


def get_current_user(token: str = Depends(ouath2_scheme)):
    creds_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Unauthorized",
                                    headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, creds_exception)
