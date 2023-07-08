from datetime import datetime
from models.product_model import SearchProduct
from services.database_service import get_collection
from utils.scrapers.amazon_search_scrapper import scrap_search_page
from utils.scrapers.pcdiga_scrapper import (
    pc_diga_price_scraper,
    pc_diga_product_info_scraper,
    pc_diga_promotion_date,
    scrap_pc_diga_url,
)
from services.message_service import message_builder, send_message
from services.price_service import save_record
from services.product_service import get_products as _get_products, update_product
import asyncio
from pprint import pprint


def scrap_pcdiga_urls():
    scraped_data = []
    urls = _get_products()
    tasks = []

    async def scrape_url(url_data):
        if url_data.store == "pcdiga":
            page_content = await asyncio.to_thread(scrap_pc_diga_url, url_data.url)
            prices = await asyncio.to_thread(pc_diga_price_scraper, page_content)
            product_name = await asyncio.to_thread(
                pc_diga_product_info_scraper, page_content
            )
            promotion_dates = (
                await asyncio.to_thread(pc_diga_promotion_date, page_content)
                if prices.discount
                else None
            )
            scraped_data.append(
                {
                    "prices": prices,
                    "url": url_data.url,
                    "product_name": product_name,
                    "promotion_data": promotion_dates,
                }
            )
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


def scrap_amazon_search_page(search_item: str):
    try:
        # just for testing purposes
        delete_all_searchs_from_amazon()

        items = scrap_search_page(search_item)

        for item in items:
            amazon_search_collection = get_collection("amazon_search")
            current_datetime = datetime.now()
            current_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            searched_product = SearchProduct(**{**item, "date": current_time})
            amazon_search_collection.insert_one(searched_product.to_dict())

        pprint(get_all_searchs_from_amazon())
        return {"message": "All data has been scraped!"}
    except Exception as e:
        raise e


def get_all_searchs_from_amazon():
    try: 
        amazon_search_collection = get_collection("amazon_search")
        return [item for item in amazon_search_collection.find({})]
    except Exception as e:
        raise e


def delete_all_searchs_from_amazon():
    amazon_search_collection = get_collection("amazon_search")
    amazon_search_collection.delete_many({})
