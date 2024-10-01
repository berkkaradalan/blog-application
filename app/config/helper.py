import uuid
import time
from pymongo import MongoClient
from app.models.collection_models import mongoDocs
from fastapi import HTTPException, Depends, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from  app.models.collection_models import userDocument, UserInDB, TokenData
from typing import Annotated
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config.dotenv import settings
import app.config.handler as handler
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_id():
    return uuid.uuid4()

def get_current_time():
    return int(time.time())

def mongo_connection():
    client = MongoClient(f"mongodb://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}@{settings.MONGO_IP}:{settings.MONGO_PORT}/")
    if(not client):
        raise handler.MongoDBExceptionHandler()
    blog_mongo = client["blog-mongo"]
    users = blog_mongo["users"]
    blogs = blog_mongo["blogs"]
    comments = blog_mongo["comments"]
    
    docs = mongoDocs(
        users=users,
        blogs=blogs,
        comments=comments,
        )
    return docs

mongo_collections = mongo_connection()

def mongo_manager():
    client = MongoClient(f"mongodb://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}@{settings.MONGO_IP}:{settings.MONGO_PORT}/")
    db = client['blog-mongo']
    if not client:
        raise handler.MongoDBExceptionHandler()
    collections = db.list_collection_names()
    if "users" not in collections:
        db.create_collection("users")
    if "blogs" not in collections:
        db.create_collection("blogs")
    if "comments" not in collections:
        db.create_collection("comments")

def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(regex, email)):
        return True 
    else:
        return False

def get_password_hash(password):
    return pwd_context.hash(password)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
access_token_expire_minutes=int(settings.ACCESS_TOKEN_EXPIRE_TIME)
algorithm=settings.ALGORITHM
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")
secret_key=settings.SECRET_KEY

def get_user(db, username: str):
    mongo_user = db.find_one({"username":username})
    if mongo_user and "username" in mongo_user:
        return UserInDB(**mongo_user)
    return None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(mongo_collections.users, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[userDocument, Depends(get_current_user)]
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user