from fastapi import APIRouter, HTTPException, Query, Request, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List
from backend.app.db.db_local import get_products_by_user_id_and_date, update_user_product
from backend.app.schemas.product_dto import ProductModel

router = APIRouter(tags=['Products'])


class DayProducts(BaseModel):
    date: str
    products: List[ProductModel]

@router.get("/api/products", response_model=DayProducts)
async def get_products(date: str):
    user_id = 1
    products = await get_products_by_user_id_and_date(user_id=user_id, date=date)

    return DayProducts(date=date, products=products)

# @router.post("/api/products/{date}", response_model=DayProducts)
# async def add_product(date: str, product: Product):
#     if date not in mock_db:
#         mock_db[date] = []
#     mock_db[date].append(product)
#     return DayProducts(date=date, products=mock_db[date])


@router.put("/api/products", response_model=ProductModel)
async def update_product(updated_product: ProductModel):
    user_id = 1
    await update_user_product(user_id=user_id, updated_product=updated_product)

    return updated_product


