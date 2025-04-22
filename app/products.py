from sqlalchemy import select,desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Product
from fastapi import APIRouter,Depends
from fastapi_cache.decorator import cache
from app.cache import redis_client
from app.auth import get_current_user
from app.schemas import Products


router=APIRouter()

@router.get("/get-products")
@cache(expire=60)
async def get_products(db:AsyncSession=Depends(get_db),current_user:dict=Depends(get_current_user)):
    print("Fetching from DB...")
    keys = await redis_client.keys("*")
    print("📦 Redis keys:", keys)
    query=select(Product).order_by(desc(Product.sales)).limit(10)
    result=await db.execute(query)
    products=result.scalars().all()
    return products



@router.post("/add-products")
async def add_products(product:Products,db:AsyncSession=Depends(get_db)):
    db_products=Product(**product.dict())
    db.add(db_products)
    await db.commit()
    await db.refresh(db_products)
    return db_products
