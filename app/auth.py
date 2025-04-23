# from datetime import timedelta, datetime
# from typing import Annotated
# from fastapi import APIRouter, Depends, HTTPException, Cookie
# from pydantic import BaseModel
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from starlette import status
# from app.database import async_session
# from app.models import User
# from passlib.context import CryptContext
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import jwt, JWTError
# from fastapi.responses import RedirectResponse
# import os
# from dotenv import load_dotenv

# load_dotenv()

# router = APIRouter(tags=['auth'])

# SECRET_KEY = os.getenv("SECRET_KEY")
# ALGORITHM = os.getenv("ALGORITHM")

# bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# # async def oauth2_bearer_from_cookie(access_token: str = Cookie(None)):
# #     if not access_token:
# #         raise HTTPException(status_code=401, detail="Not authenticated")
# #     return access_token

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# class CreateUserRequest(BaseModel):
#     username: str
#     password: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# async def get_db():
#     async with async_session() as session:
#         yield session

# db_dependency = Annotated[AsyncSession, Depends(get_db)]

# def hash_password(password):
#     return bcrypt_context.hash(password)

# @router.post("/", status_code=status.HTTP_201_CREATED)
# async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    
#     query = select(User).where(User.username == create_user_request.username)
#     result = await db.execute(query)
#     if result.scalar_one_or_none():
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Username already exists"
#         )
    
#     new_user = User(
#         username=create_user_request.username,
#         hashed_password=hash_password(create_user_request.password),
#     )
#     db.add(new_user)
#     await db.commit()
#     return {"message": "User created successfully"}

# @router.post("/token", response_model=Token)
# async def login_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
#     db: db_dependency
# ):
#     user = await authenticate_user(form_data.username, form_data.password, db)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail='Could not validate user'
#         )
#     token = create_access_token(user.username, user.id, timedelta(minutes=30))
#     return {'access_token': token, 'token_type': 'bearer'}

# async def authenticate_user(username: str, password: str, db: AsyncSession):
#     query = select(User).where(User.username == username)
#     result = await db.execute(query)
#     user = result.scalar_one_or_none()
    
#     if not user:
#         return False
#     if not bcrypt_context.verify(password, user.hashed_password):
#         return False
#     return user

# def create_access_token(username: str, user_id: int, expires_delta: timedelta):
#     encode = {'sub': username, 'id': user_id}
#     expires = datetime.utcnow() + expires_delta
#     encode.update({'exp': expires})
#     return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# # async def get_current_user(token: str = Depends(oauth2_scheme)):
# #     try:
# #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
# #         username: str = payload.get('sub')
# #         user_id: int = payload.get('id')
# #         if username is None or user_id is None:
# #             raise HTTPException(status_code=401, detail="Invalid token payload")
# #         return {"username": username, "user_id": user_id}
# #     except JWTError as e:
# #         print("JWT Error:", str(e)) 
# #         raise HTTPException(status_code=401, detail="Could not validate credentials")


# async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid authentication credentials"
#             )
#         query=select(User).where(User.username==username)
#         result=await db.execute(query)

#         user = result.scalar_one_or_none()
#         if user is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="User not found"
#             )
#         return user
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token"
#         )

# @router.post("/logout")
# async def logout():
#     response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
#     response.delete_cookie("access_token")
#     return response




from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Cookie
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.database import async_session
from app.models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from fastapi.responses import RedirectResponse
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix='/auth', tags=['auth'])

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# async def oauth2_bearer_from_cookie(access_token: str = Cookie(None)):
#     if not access_token:
#         raise HTTPException(status_code=401, detail="Not authenticated")
#     return access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

async def get_db():
    async with async_session() as session:
        yield session

db_dependency = Annotated[AsyncSession, Depends(get_db)]

def hash_password(password):
    return bcrypt_context.hash(password)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    
    query = select(User).where(User.username == create_user_request.username)
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    new_user = User(
        username=create_user_request.username,
        hashed_password=hash_password(create_user_request.password),
    )
    db.add(new_user)
    await db.commit()
    return {"message": "User created successfully"}

@router.post("/token", response_model=Token)
async def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user'
        )
    token = create_access_token(user.username, user.user_id, timedelta(minutes=30))
    return {'access_token': token, 'token_type': 'bearer'}

async def authenticate_user(username: str, password: str, db: AsyncSession):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return {"username": username, "user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

@router.post("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")
    return response