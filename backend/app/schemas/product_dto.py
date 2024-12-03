from datetime import datetime

from pydantic import BaseModel
from sqlalchemy.util import symbol


class Info(BaseModel):
    carbohydrates: float
    proteins: float
    fats: float


class RecognizingProductDto(BaseModel):
    name: str
    kkal: float
    detail: Info
    prompt: list[str]


class ProductModel(BaseModel):
    id: str
    name: str
    calories: int
    protein: float
    fats: float
    carbs: float
    date: datetime
    image: str
    weight: float
    recommends: list[str]