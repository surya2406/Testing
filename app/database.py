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
import os
import sys

# Debug: Print all environment variables
print("===== AVAILABLE ENVIRONMENT VARIABLES =====", file=sys.stderr)
for key, value in os.environ.items():
    # Hide passwords but show all variable names
    masked_value = "****" if "PASSWORD" in key.upper() else value
    print(f"{key}: {masked_value}", file=sys.stderr)
print("=========================================", file=sys.stderr)

# Directly try different variable options
mysql_url = os.environ.get("MYSQL_URL")
mysql_url_lowercase = os.environ.get("mysql_url")
mysql_host = os.environ.get("MYSQLHOST")

print(f"Direct access - MYSQL_URL: {'Found' if mysql_url else 'Not Found'}", file=sys.stderr)
print(f"Direct access - mysql_url: {'Found' if mysql_url_lowercase else 'Not Found'}", file=sys.stderr)
print(f"Direct access - MYSQLHOST: {'Found' if mysql_host else 'Not Found'}", file=sys.stderr)

# Try to construct URL from components
try:
    mysql_host = os.environ.get("MYSQLHOST")
    mysql_port = os.environ.get("MYSQLPORT", "3306") 
    mysql_database = os.environ.get("MYSQLDATABASE")
    mysql_user = os.environ.get("MYSQLUSER")
    mysql_password = os.environ.get("MYSQLPASSWORD")
    
    constructed_url = None
    if all([mysql_host, mysql_database, mysql_user, mysql_password]):
        constructed_url = f"mysql+aiomysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"
        print(f"Constructed URL: {constructed_url.replace(mysql_password, '****')}", file=sys.stderr)
    else:
        print("Cannot construct URL, missing components:", file=sys.stderr)
        print(f"  MYSQLHOST: {'Found' if mysql_host else 'Missing'}", file=sys.stderr)
        print(f"  MYSQLPORT: {'Found' if mysql_port else 'Missing'}", file=sys.stderr)
        print(f"  MYSQLDATABASE: {'Found' if mysql_database else 'Missing'}", file=sys.stderr)
        print(f"  MYSQLUSER: {'Found' if mysql_user else 'Missing'}", file=sys.stderr)
        print(f"  MYSQLPASSWORD: {'Found' if mysql_password else 'Missing'}", file=sys.stderr)
    
    # Use constructed URL if available, otherwise try MYSQL_URL
    URL_DATABASE = constructed_url or mysql_url
    
    # Still nothing? Try Railway's DATABASE_URL
    if not URL_DATABASE:
        URL_DATABASE = os.environ.get("DATABASE_URL")
        print(f"Trying DATABASE_URL: {'Found' if URL_DATABASE else 'Not Found'}", file=sys.stderr)
    
    if not URL_DATABASE:
        print("CRITICAL: No database URL could be found or constructed", file=sys.stderr)
        raise ValueError("No database URL found after trying all options.")
    
    # Create engine and session
    print(f"Using URL: {URL_DATABASE.replace(mysql_password if mysql_password else '', '****')}", file=sys.stderr)
    engine = create_async_engine(URL_DATABASE, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async def get_db():
        async with async_session() as db:
            try:
                yield db
            finally:
                await db.close()
    
    Base = declarative_base()

except Exception as e:
    print(f"CRITICAL ERROR: {str(e)}", file=sys.stderr)
    raise
