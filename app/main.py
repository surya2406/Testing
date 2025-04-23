from datetime import timedelta
from fastapi import FastAPI,Depends,HTTPException,status
import uvicorn
from app.cache import init_cache
from app.products import router as product_router
from app.database import AsyncSession,engine,Base,get_db
from app.cache import init_cache,redis_client
from sqlalchemy import select 
from app.auth import CreateUserRequest,hash_password
from app.models import User
from app.auth import router as authrouter
from fastapi.middleware.cors import CORSMiddleware
from app.auth import create_access_token,OAuth2PasswordRequestForm,bcrypt_context
from dotenv import load_dotenv
import os
from prometheus_fastapi_instrumentator import Instrumentator

load_dotenv()

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)
app.include_router(product_router)
app.include_router(authrouter)

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init_cache()
@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()



@app.post("/signup")
async def signup(user:CreateUserRequest,db:AsyncSession=Depends(get_db)):
    query=select(User).where(User.username==user.username)
    result=await db.execute(query)
    existing_user=result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already registered.")
    password=hash_password(user.password)
    new_user=User(username=user.username,hashed_password=password)
    db.add(new_user)
    await db.commit()
    return {"Message":"User created successfully!"}

@app.post("/login")
async def login(form_data:OAuth2PasswordRequestForm=Depends(), db:AsyncSession=Depends(get_db)):
    query=select(User).where(User.username==form_data.username)
    result=await db.execute(query)
    user=result.scalar_one_or_none()
    if not user or not bcrypt_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")
    access_token=create_access_token(user.username, user.user_id, timedelta(minutes=30))
    return {'access_token': access_token, 'token_type': 'bearer'}


if __name__ == "__main__":
    uvicorn.run("your_app:app", host="0.0.0.0", port=8000)
