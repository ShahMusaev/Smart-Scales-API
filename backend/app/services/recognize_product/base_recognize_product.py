from backend.app.schemas.product_dto import RecognizingProductDto
from abc import ABC, abstractmethod

# {
#   "название продукта": "Яблоко",
#   "ккал на 100 грамм": 52,
#   "бжу": {
#     "белки": 0.3,
#     "жиры": 0.2,
#     "углеводы": 14
#   },
#   "рекомендации по приготовлению": "Яблоко можно есть сырым, добавлять в салаты или использовать для выпечки."
# }

class BaseRecognizeProduct(ABC):
    def __init__(self):
        ...

    @abstractmethod
    async def get_product_info_by_img(self, img_url: str) -> RecognizingProductDto:
        ...
