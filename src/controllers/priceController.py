from fastapi import APIRouter
from services.price_service import clear_prices_record as _clear_prices_record, get_all_records as _get_all_records
from services.scraper_service import scrap_urls as _scrap_urls

priceRouter = APIRouter(prefix="/price", tags=["Price"])

@priceRouter.get("/updates")
def get_price_update():
    return _scrap_urls()

@priceRouter.get("")
def get_prices_record():
    return _get_all_records()

@priceRouter.delete("")
def clear_prices_record():
    _clear_prices_record()
    return {"message": "All records were deleted successfully"}
