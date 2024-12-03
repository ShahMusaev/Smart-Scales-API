import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime

from backend.app.schemas.product_dto import RecognizingProductDto, ProductModel
from backend.app.services.recognize_product.base_recognize_product import BaseRecognizeProduct
from backend.app.services.recognize_product.gpt.gpt_recognize_product import GPTRecognizeProduct
from backend.app.services.unload_img.base_unload_service import BaseUnloadService
from backend.app.services.unload_img.storage.storage import StorageUnloadService
from backend.app.db.db_local import add_user_product

router = APIRouter(tags=['Recognizing'])


class RecognizingProductReq(BaseModel):
    date: datetime
    img_base64: str
    weight: float


class RecognizingProductRes(BaseModel):
    name: str
    calories: int
    protein: float
    fats: float
    carbs: float
    date: datetime
    image: str
    weight: float


@router.post("/api/recognizing/products", response_model=RecognizingProductRes)
async def recognizing_product(
        rec_product_req: RecognizingProductReq,
        rec_service: BaseRecognizeProduct = Depends(GPTRecognizeProduct),
        unload_service: BaseUnloadService = Depends(StorageUnloadService)
):
    user_id = 1
    product_id = str(uuid.uuid4())
    img_name = f'{user_id}/{datetime.now().strftime("%Y-%m-%d")}/{product_id}'
    img_url = await unload_service.unload_img(img_base64=rec_product_req.img_base64, img_name=img_name)
    product: RecognizingProductDto = await rec_service.get_product_info_by_img(img_url)
    weight = rec_product_req.weight

    product_db = ProductModel(
        id=product_id,
        name=product.name,
        calories=int(product.kkal * (weight / 100)),
        protein=product.detail.proteins * (weight / 100),
        fats=product.detail.fats * (weight / 100),
        carbs=product.detail.carbohydrates * (weight / 100),
        date=rec_product_req.date,
        image=img_url,
        weight=rec_product_req.weight,
        recommends=product.prompt
    )

    await add_user_product(user_id, product_db)


    return RecognizingProductRes(
        name=product.name,
        calories=int(product.kkal * (weight / 100)),
        protein=product.detail.proteins * (weight / 100),
        fats=product.detail.fats * (weight / 100),
        carbs=product.detail.carbohydrates * (weight / 100),
        date=rec_product_req.date,
        image=img_url,
        weight=rec_product_req.weight
    )
