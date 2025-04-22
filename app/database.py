from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
import os

load_dotenv()

URL_DATABASE = os.getenv("DATABASE_URL", "").replace("mysql://", "mysql+aiomysql://")
engine=create_async_engine(URL_DATABASE,echo=True)
async_session=sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)

async def get_db():
    async with async_session() as db:
        try:
            yield db
        finally:
            await db.close()

Base=declarative_base()