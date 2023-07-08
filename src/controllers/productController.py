from fastapi import APIRouter
from services.product_service import (
    create_product as _create_product,
    delete_products as _delete_products,
    get_products as _get_products,
    delete_product_by_uuid as _delete_product_by_uuid,
    delete_all_products_from_store as _delete_products_by_store
)
from models.product_model import Product, ProductBody, ProductDTO
from typing import List

productRouter = APIRouter(prefix="/product", tags=["Product"])


@productRouter.get("")
def get_all_products() -> List[ProductDTO]:
    return _get_products()

@productRouter.get("/{store_name}")
def get_products_by_store(store_name: str) -> List[ProductDTO]:
    return _get_products(store_name)


@productRouter.delete("")
def delete_all_products() -> dict:
    return _delete_products()

@productRouter.delete("/{store_name}")
def delete_products_by_store(store_name: str) -> dict:
    return _delete_products_by_store(store_name)


@productRouter.delete("/{product_uuid}")
def delete_product_by_uuid(product_uuid: str) -> dict:
    return _delete_product_by_uuid(product_uuid)


@productRouter.post("")
def create_product(url: ProductBody) -> dict:
    return _create_product(url)


