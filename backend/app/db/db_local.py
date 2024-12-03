from backend.app.schemas.product_dto import ProductModel
from typing import List

mock_db = {}

async def get_products_by_user_id_and_date(user_id: int, date: str) -> List[ProductModel]:
    if user_id not in mock_db:
        return []

    if date not in mock_db[user_id]:
        return []

    products_json = mock_db[user_id][date]
    list_product = []
    for product_js in products_json:
        product = ProductModel(
            id=product_js.get('id'),
            name=product_js.get('name'),
            calories=product_js.get('calories'),
            protein=product_js.get('protein'),
            fats=product_js.get('fats'),
            carbs=product_js.get('carbs'),
            date=product_js.get('date'),
            image=product_js.get('image'),
            weight=product_js.get('weight'),
            recommends=product_js.get('recommends'),
        )
        list_product.append(product)

    return list_product

async def add_user_product(user_id, product: ProductModel):
    if user_id not in mock_db:
        mock_db[user_id] = {}

    date = product.date.strftime("%Y-%m-%d")
    if date not in mock_db[user_id]:
        mock_db[user_id][date] = []

    mock_db[user_id][date].append(product.__dict__)
    print(mock_db)

async def find_user_product(user_id: str, product_id: str) -> ProductModel:
    if user_id not in mock_db:
        raise Exception('User not find')

    dates = mock_db[user_id]

    for date in dates:
        product_list = mock_db[user_id][date]
        for i, product in enumerate(product_list):
            if product.get('id') == product_id:
                return ProductModel(
                    id=product.get('name'),
                    name=product.get('name'),
                    calories=product.get('calories'),
                    protein=product.get('protein'),
                    fats=product.get('fats'),
                    carbs=product.get('carbs'),
                    date=product.get('date'),
                    image=product.get('image'),
                    weight=product.get('weight'),
                )

    return None

async def update_user_product(user_id: int, updated_product: ProductModel):
    if user_id not in mock_db:
        raise Exception('User not find')

    dates = mock_db[user_id]

    for date in dates:
        product_list = mock_db[user_id][date]
        for i, product in enumerate(product_list):
            if product.get('id') == updated_product.id:
                mock_db[user_id][date][i] = updated_product.__dict__

