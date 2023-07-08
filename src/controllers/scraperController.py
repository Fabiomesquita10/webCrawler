from fastapi import APIRouter

from services.scraper_service import scrap_amazon_search_page, scrap_pcdiga_urls
from utils.scrapers.amazon_search_scraper import scrap_search_page

scraperRouter = APIRouter(prefix="/scrap", tags=["Scraper"])

@scraperRouter.get("/pcDiga")
def test_scraper_pc_diga():
    return scrap_pcdiga_urls()

@scraperRouter.get("/amazon/{search_item}")
def test_scraper_amazon(search_item: str):
    return scrap_amazon_search_page(search_item)