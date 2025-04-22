# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
# from sqlalchemy.ext.declarative import declarative_base

# from dotenv import load_dotenv
# import os

# load_dotenv()

# URL_DATABASE = os.getenv("DATABASE_URL")
# engine=create_async_engine(URL_DATABASE,echo=True)
# async_session=sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)

# async def get_db():
#     async with async_session() as db:
#         try:
#             yield db
#         finally:
#             await db.close()

# Base=declarative_base()


from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Option 1: Use the complete MYSQL_URL variable (preferred)
URL_DATABASE = os.getenv("MYSQL_URL")

# Option 2: If MYSQL_URL isn't working, construct from individual components
if not URL_DATABASE:
    mysql_host = os.getenv("MYSQLHOST")
    mysql_port = os.getenv("MYSQLPORT")
    mysql_database = os.getenv("MYSQLDATABASE")
    mysql_user = os.getenv("MYSQLUSER")
    mysql_password = os.getenv("MYSQLPASSWORD")
    
    if all([mysql_host, mysql_database, mysql_user, mysql_password]):
        # Make sure to use the correct driver prefix for async operations
        URL_DATABASE = f"mysql+aiomysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"

# Validate we have a database URL before proceeding
if not URL_DATABASE:
    raise ValueError("No MySQL database URL found. Please check your environment variables.")

# Create engine and session
engine = create_async_engine(URL_DATABASE, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session() as db:
        try:
            yield db
        finally:
            await db.close()

Base = declarative_base()
