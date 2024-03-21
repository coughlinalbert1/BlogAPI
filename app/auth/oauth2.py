from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from ..db.database import get_db
from ..db import db_user
from fastapi import HTTPException, status

# This doesnt create the endpoint but says this endpoint will be required to recieve token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token') # tokenUrl is the endpoint where the user will send their username and password to get a token

SECRET_KEY = '654acd23c83c1cf81e93fda6674cdda88d244a22546067bee905e68e5b776bde'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db_user.get_user_by_username(db, username)

    if user is None:
        raise credentials_exception
    
    return user


