from fastapi import APIRouter, Path, Query
from services.product_service import (
    create_product as _create_product,
    delete_products as _delete_products,
    get_product_by_uuid as _get_product_by_uuid,
    get_products as _get_products,
    delete_product_by_uuid as _delete_product_by_uuid,
    delete_all_products_from_store as _delete_products_by_store,
    update_product as _update_product,
)
from models.product_model import ProductUpdate, Product, ProductBody, ProductDTO
from typing import List
from fastapi.responses import JSONResponse

productRouter = APIRouter(prefix="/product", tags=["Product"])


@productRouter.get("")
def get_all_products(
    page: int = Query(default=1, gt=0), page_size: int = Query(default=10, gt=0)
) -> List[ProductDTO]:
    return _get_products(store=None, page=page, page_size=page_size)


@productRouter.get("/store/{store_name}")
def get_products_by_store(
    store_name: str,
    page: int = Query(default=1, gt=0),
    page_size: int = Query(default=10, gt=0),
) -> List[ProductDTO]:
    return _get_products(store_name, page=page, page_size=page_size)


@productRouter.get("/{product_uuid}")
def get_product_by_product_uuid(product_uuid: str) -> ProductDTO:
    return _get_product_by_uuid(product_uuid)


@productRouter.delete("")
def delete_all_products() -> JSONResponse:
    return _delete_products()


@productRouter.delete("/store/{store_name}")
def delete_products_by_store(store_name: str) -> JSONResponse:
    return _delete_products_by_store(store_name)


@productRouter.delete("/{product_uuid}")
def delete_product_by_uuid(product_uuid: str) -> JSONResponse:
    return _delete_product_by_uuid(product_uuid)


@productRouter.post("")
def create_product(product: ProductBody) -> ProductDTO:
    return _create_product(product)


@productRouter.patch("/{product_uuid}")
def update_product(product: ProductUpdate, product_uuid: str) -> ProductDTO:
    return _update_product(product, product_uuid)
