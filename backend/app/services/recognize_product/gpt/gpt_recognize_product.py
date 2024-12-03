from backend.app.services.recognize_product.gpt.client import AsyncOpenAI
from backend.app.schemas.product_dto import RecognizingProductDto
from backend.app.schemas.product_dto import Info
from backend.app.services.recognize_product.base_recognize_product import BaseRecognizeProduct
from backend.config.config import config
import json

PROXY_HOST = config.PROXY_HOST
proxy_port = config.PROXY_PORT
PROXY_USER = config.PROXY_USER
PROXY_PAS = config.PROXY_PWD

PROMPT = 'Напиши какой продукт на фотографии, в формате json с полями - "название продукта", "ккал на 100 грамм", "бжу"- {"белки", "жиры", "углеводы"}, "рекомендации по приготовлению". Рекомендации по приготовлению должен быть в виде массива из 4 советов. Пожалуйста, напиши только json, без лишних комментариев'


class GPTRecognizeProduct(BaseRecognizeProduct):
    def __init__(self):
        self._api_key = config.OPENAI_API_KEY
        self._model = 'gpt-4o'

        super().__init__()

    async def get_product_info_by_img(self, img_url: str) -> RecognizingProductDto:
        proxies = f'http://{PROXY_USER}:{PROXY_PAS}@{PROXY_HOST}:{proxy_port}'
        client = AsyncOpenAI(api_key=self._api_key, proxies=proxies)

        completion = await client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text",
                         "text": PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": img_url,
                            }
                        },
                    ],
                }
            ],
        )

        res_str = completion.choices[0].message.content
        json_res = json.loads(res_str.replace('```json', '').replace('```', ''))
        print(json_res)

        info = Info(
            carbohydrates=float(json_res.get('бжу', {}).get('углеводы')),
            proteins=float(json_res.get('бжу', {}).get('белки')),
            fats=float(json_res.get('бжу', {}).get('жиры')),
        )

        return RecognizingProductDto(
            name=json_res.get("название продукта"),
            kkal=float(json_res.get("ккал на 100 грамм")),
            detail=info,
            prompt=json_res.get("рекомендации по приготовлению"),
        )
