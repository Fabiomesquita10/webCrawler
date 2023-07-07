from playwright.sync_api import sync_playwright
from utils.scrapers.pcdiga_scrapper import (
    pc_diga_price_scraper,
    pc_diga_product_info_scraper,
    pc_diga_promotion_date,
)
from services.message_service import message_builder, send_message
from services.price_service import save_record
from services.product_service import get_products as _get_products, update_product
import asyncio


def scrap(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()
        page.goto(url)
        html_content = page.inner_html(
            "body"
        )  # Get the inner HTML of the <html> element
        return html_content


def scrap_urls():
    scraped_data = []
    urls = _get_products()
    tasks = []
    
    async def scrape_url(url_data):
        if url_data.store == "pcdiga":
            page_content = await asyncio.to_thread(scrap, url_data.url)
            prices = await asyncio.to_thread(pc_diga_price_scraper, page_content)
            product_name = await asyncio.to_thread(pc_diga_product_info_scraper, page_content)
            promotion_dates = await asyncio.to_thread(pc_diga_promotion_date, page_content) if prices.discount else None
            scraped_data.append({
                "prices": prices,
                "url": url_data.url,
                "product_name": product_name,
                "promotion_data": promotion_dates,
            })
            update_product(url_data, product_name)
        else:
            print("Invalid store!")
    
    async def run_tasks():
        for url_data in urls:
            task = asyncio.ensure_future(scrape_url(url_data))
            tasks.append(task)
        await asyncio.gather(*tasks)

    asyncio.run(run_tasks())

    save_record(scraped_data)
    message = message_builder(scraped_data)
    send_message(message, True)
    return "Check your messages!"
