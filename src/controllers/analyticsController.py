from fastapi import APIRouter
from services.analytics_service import (
    delete_records,
    get_all_records_from_search,
    get_product_analytics as _get_product_analytics
)

analyticsRouter = APIRouter(prefix="/analytics", tags=["Analytics"])


@analyticsRouter.get("/{product_uuid}")
def get_product_analytics(product_uuid: str):
    return _get_product_analytics(product_uuid)


@analyticsRouter.get("/store/{store}/item/{searched_item}")
def get_search_product_analytics(store: str, searched_item: str):
    # TODO: return all records from a search on a given store
    return get_all_records_from_search(searched_item, store)

    
@analyticsRouter.delete("/")
def delete_all_analytics_records():
    return delete_records()