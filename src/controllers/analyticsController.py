from pprint import pprint
from fastapi import APIRouter
from services.analytics_service import (
    get_all_records_from_search_input,
    get_records_from_product_by_store,
)

analyticsRouter = APIRouter(prefix="/analytics", tags=["Analytics"])


@analyticsRouter.get("/product/{product_uuid}")
def get_product_analytics(product_uuid: str):
    # TODO: return all records from a scraped product
    return


@analyticsRouter.get("/store/{store}/item/{searched_item}")
def get_search_product_analytics(store: str, searched_item: str):
    # TODO: return all records from a search on a given store
    return get_records_from_product_by_store(searched_item, store)


@analyticsRouter.get("/store/{store}")
def get_searchs_by_store_analytics(store: str):
    # TODO: return all records from a given store
    return get_all_records_from_search_input(store)
    
