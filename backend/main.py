import uvicorn
from app.api import app

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8076, log_level='info')
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from datetime import datetime, timedelta
# import uvicorn
# from typing import List
#
# from starlette.middleware.cors import CORSMiddleware
#
# app = FastAPI()
#
# origins = ["*"]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# # This is a mock database. In a real application, you'd use a proper database.
# mock_db = {}
#
#
# class Product(BaseModel):
#     name: str
#     calories: float
#     protein: float
#     fats: float
#     carbs: float
#     time: str
#     image: str
#     weight: float
#
#
# class DayProducts(BaseModel):
#     date: str
#     products: List[Product]
#
#
# # Populate mock database with some data
# today = datetime.now().date()
# mock_db[str(today)] = [
#     Product(name="Orange", calories=62, protein=1.2, fats=0.2, carbs=15.4, time="16:01",
#             image="https://storage.yandexcloud.net/itmo-smart-sacles/apple.jpg", weight=130),
#     Product(name="Fresh Bananas", calories=210, protein=2.6, fats=0.6, carbs=54, time="16:00",
#             image="https://storage.yandexcloud.net/itmo-smart-sacles/banan.jpg", weight=225)
# ]
#
# mock_db[str(today - timedelta(days=1))] = [
#     Product(name="Apple", calories=95, protein=0.5, fats=0.3, carbs=25, time="12:30",
#             image="https://storage.yandexcloud.net/itmo-smart-sacles/apple.jpg", weight=182),
#     Product(name="Yogurt", calories=150, protein=8, fats=3.5, carbs=17, time="08:15",
#             image="/placeholder.svg?height=80&width=80", weight=200)
# ]
#
#
# @app.get("/api/products/{date}", response_model=DayProducts)
# async def get_products(date: str):
#     if date not in mock_db:
#         raise HTTPException(status_code=404, detail="No data for this date")
#     return DayProducts(date=date, products=mock_db[date])
#
#
# @app.post("/api/products/{date}", response_model=DayProducts)
# async def add_product(date: str, product: Product):
#     if date not in mock_db:
#         mock_db[date] = []
#     mock_db[date].append(product)
#     return DayProducts(date=date, products=mock_db[date])
#
#
# @app.put("/api/products/{date}/{product_name}", response_model=Product)
# async def update_product(date: str, product_name: str, updated_product: Product):
#     if date not in mock_db:
#         raise HTTPException(status_code=404, detail="No data for this date")
#
#     for i, product in enumerate(mock_db[date]):
#         if product.name == product_name:
#             mock_db[date][i] = updated_product
#             return updated_product
#
#     raise HTTPException(status_code=404, detail="Product not found")
#
#
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
