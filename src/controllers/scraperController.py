from fastapi import APIRouter

from services.scraper_service import scrap_amazon_product, scrap_amazon_search_page, scrap_amazon_urls, scrap_pcdiga_urls, scrap_product_from_cart

scraperRouter = APIRouter(prefix="/scrap", tags=["Scraper"])

@scraperRouter.get("/pcDiga")
def test_scraper_pc_diga():
    return scrap_pcdiga_urls()

@scraperRouter.get("/amazon")
def test_scraper_amazon():
    return scrap_amazon_urls()

@scraperRouter.get("/amazon/{search_item}")
def test_scraper_amazon(search_item: str):
    return scrap_amazon_search_page(search_item)


@scraperRouter.get("/amazon/product/{product_uuid}")
def test_scraper_amazon(product_uuid: str):
    return scrap_amazon_product(product_uuid)

@scraperRouter.get("/cart/{cart_uuid}")
def test_scrap_cart(cart_uuid: str):
    return scrap_product_from_cart(cart_uuid)