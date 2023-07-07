from fastapi import APIRouter
from services.product_service import (
    create_product as _create_product,
    delete_products as _delete_products,
    get_products as _get_products,
    delete_product_by_uuid as _delete_product_by_uuid
)
from models.product_model import Product, ProductBody, ProductDTO
from typing import List

urlRouter = APIRouter(prefix="/product", tags=["Product"])


@urlRouter.get("")
def get_products() -> List[ProductDTO]:
    return _get_products()


@urlRouter.delete("")
def delete_all_products() -> dict:
    return _delete_products()


@urlRouter.delete("/{product_uuid}")
def delete_product_by_uuid(product_uuid: str) -> dict:
    return _delete_product_by_uuid(product_uuid)


@urlRouter.post("")
def create_product(url: ProductBody) -> dict:
    return _create_product(url)
