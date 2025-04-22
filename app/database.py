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

# Get database URL
URL_DATABASE = os.getenv("DATABASE_URL")

# If empty, use a hardcoded value as fallback (for development only)
if not URL_DATABASE:
    URL_DATABASE = "mysql+aiomysql://root:WAVXSeQyJbIsalRxOmmVGhuBprXQlvWj@mysql.railway.internal:3306/railway"

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
