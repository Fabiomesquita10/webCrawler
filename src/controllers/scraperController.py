from fastapi import APIRouter

from services.scraper_service import scrap_urls
from utils.scrapers.amazon_scrapper import scrap_search_page

scraperRouter = APIRouter(prefix="/scrap", tags=["Scraper"])

@scraperRouter.get("/pcDiga")
def test_scraper_pc_diga():
    return scrap_urls()

@scraperRouter.get("/amazon/{search_item}")
def test_scraper_amazon(search_item: str):
    return scrap_search_page(search_item)