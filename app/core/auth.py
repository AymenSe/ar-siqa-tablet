# app/core/auth.py
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..config import settings
from .. import models
from .security import verify_password

# For JWT, install: pip install "python-jose[cryptography]"
# This example uses synchronous code for brevity.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(db: Session, username: str, password: str):
    subject = db.query(models.Subject).filter(models.Subject.username == username).first()
    if not subject:
        return None
    if not verify_password(password, subject.password_hash):
        return None
    return subject


def get_current_subject(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    This function will parse the token, verify it, 
    and return the authenticated Subject from the DB.
    You can adapt how you pass the token (bearer header, cookie, etc.).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    subject = db.query(models.Subject).filter(models.Subject.username == username).first()
    if subject is None:
        raise credentials_exception
    return subject
