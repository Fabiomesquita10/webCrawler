from fastapi import APIRouter
from services.analytics_service import (
    delete_records,
    get_all_records_from_search,
    get_product_analytics as _get_product_analytics,
    get_product_analytics_by_cart as _get_product_analytics_by_cart
)

analyticsRouter = APIRouter(prefix="/analytics", tags=["Analytics"])


@analyticsRouter.get("/{product_uuid}")
def get_product_analytics(product_uuid: str):
    return _get_product_analytics(product_uuid)

@analyticsRouter.get("/cart/{cart_uuid}")
def get_product_analytics_by_cart(cart_uuid: str):
    return _get_product_analytics_by_cart(cart_uuid)

@analyticsRouter.get("/store/{store}/item/{search_input}")
def get_search_product_analytics(store: str, search_input: str):
    return get_all_records_from_search(search_input, store)

    
@analyticsRouter.delete("/")
def delete_all_analytics_records():
    return delete_records()