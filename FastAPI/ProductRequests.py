from fastapi import FastAPI
from typing import List


app = FastAPI()


sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]


# Приложение FastAPI, которое обрабатывает запросы, связанные с товарами.
@app.get('/product/search')
def search_products(keyword: str, category: str | None = None, limit: int | None = 10) -> List[dict]:
    # Фильтрация товара по ключевому слову
    filtered_products = [
        product for product in sample_products
        if keyword.lower() in product["name"].lower()
    ]

    # Фильтрация товара по категории, если она есть
    if category:
        filtered_products = [
            product for product in sample_products
            if product["category"].lower() == category.lower()
        ]

    return filtered_products[:limit]


# Получение информации о товаре по его ID
@app.get('/product/{product_id}')
def get_information(product_id: int) -> dict:
    for product in sample_products:
        if product_id == product['product_id']:
            return product
    return {"error": "Product not found"}
