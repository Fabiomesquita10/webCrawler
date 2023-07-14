from datetime import datetime
from pprint import pprint
from models.cart_model import Cart
from models.product_model import ProductBody, SearchProduct
from services.database_service import get_collection
from utils.helpers import (
    check_if_product_exist_by_name as _check_if_product_exist_by_name,
    get_cart_by_uuid as _get_cart_by_uuid,
    get_product_by_uuid as _get_product_by,
    save_image as _save_image,
    save_search as _save_search,
)
from utils.amazon_search_scraper import (
    amazon_price_scraper as _amazon_price_scraper,
    scrap_amazon_url as _scrap_amazon_url,
    scrap_search_page as _scrap_search_page,
)
from utils.pcdiga_scraper import (
    pc_diga_price_scraper as _pc_diga_price_scraper,
    pc_diga_product_info_scraper as _pc_diga_product_info_scraper,
    pc_diga_promotion_date as _pc_diga_promotion_date,
    scrap_pc_diga_url as _scrap_pc_diga_url,
)
from services.product_service import (
    update_product as _update_product,
    create_product as _create_product,
)
from utils.helpers import get_products as _get_products

import asyncio
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status


def scrap_pcdiga_urls():
    scraped_data = []
    urls = _get_products("pcdiga")
    tasks = []

    async def scrape_url(url_data):
        if url_data.store == "pcdiga":
            page_content = await asyncio.to_thread(_scrap_pc_diga_url, url_data.url)
            prices = await asyncio.to_thread(_pc_diga_price_scraper, page_content)
            product_name = await asyncio.to_thread(
                _pc_diga_product_info_scraper, page_content
            )
            promotion_dates = (
                await asyncio.to_thread(_pc_diga_promotion_date, page_content)
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
            _update_product(url_data, product_name)
        else:
            print("Invalid store!")

    async def run_tasks():
        for url_data in urls:
            task = asyncio.ensure_future(scrape_url(url_data))
            tasks.append(task)
        await asyncio.gather(*tasks)

    asyncio.run(run_tasks())

    _save_search(scraped_data)
    # message = message_builder(scraped_data)
    # send_message(message, True)
    return "Check your messages!"


def scrap_pcdiga_search_page(search_item: str):
    return


def scrap_pcdiga_product(product_uuid: str):
    return


def scrap_amazon_urls():
    scraped_data = []
    urls = _get_products("amazon")
    tasks = []

    async def scrape_url(url_data):
        if url_data.store == "amazon":
            page_content = await asyncio.to_thread(_scrap_amazon_url, url_data.url)
            prices = await asyncio.to_thread(_amazon_price_scraper, page_content)
            if prices != None:
                scraped_data.append(
                    {
                        "prices": prices,
                        "url": url_data.url,
                        "product_name": url_data.product_name,
                        "promotion_data": None,
                    }
                )
        else:
            print("Invalid store!")

    async def run_tasks():
        for url_data in urls:
            task = asyncio.ensure_future(scrape_url(url_data))
            tasks.append(task)
        await asyncio.gather(*tasks)

    asyncio.run(run_tasks())

    _save_search(scraped_data)

    return "Check your messages!"


def scrap_amazon_search_page(search_item: str):
    try:
        items = _scrap_search_page(search_item)
        for item in items:
            amazon_search_collection = get_collection("amazon_search")
            current_datetime = datetime.now()
            current_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            searched_product = SearchProduct(
                **{**item, "date": current_time, "search_product": search_item}
            )

            if not _check_if_product_exist_by_name(searched_product.title):
                url = "https://www.amazon.es" + searched_product.url
                _create_product(
                    ProductBody(
                        url=url,
                        store="amazon",
                    ),
                    searched_product.uuid,
                    searched_product.title,
                )
                _save_image(item["image"], searched_product.uuid)
                amazon_search_collection.insert_one(searched_product.to_dict())

        return JSONResponse(
            content={"message": "All products updated!"},
            status_code=status.HTTP_201_CREATED,
        )

    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error."},
        )


def scrap_amazon_product(product_uuid: str):
    product = _get_product_by(product_uuid)
    if product["store"] == "amazon":
        page_content = _scrap_amazon_url(product["url"])
        prices = _amazon_price_scraper(page_content)
        data = {
            "prices": prices if prices else None,
            "url": product["url"],
            "product_name": product["product_name"],
            "promotion_data": None,
        }
        _save_search([data])
    return


def scrap_product_from_cart(cart_uuid: str):
    tasks = []

    async def scrap_cart_uuid(product_uuid: str, store: str):
        if store == "amazon":
            await asyncio.to_thread(scrap_amazon_product, product_uuid)
        if store == "pcdiga":
            await asyncio.to_thread(scrap_pcdiga_product, product_uuid)

    async def run_tasks():
        products = Cart(**_get_cart_by_uuid(cart_uuid)).get_all_products_uuids()
        for product in products:
            for store, product_uuid in product.items():
                task = asyncio.ensure_future(
                    scrap_cart_uuid(product_uuid=product_uuid, store=store)
                )
                tasks.append(task)
        await asyncio.gather(*tasks)

    asyncio.run(run_tasks())

    return {"message": "Items scrapped!"}
