from models.price_model import PriceDTO
from models.product_model import SearchProduct
from services.database_service import get_collection
from services.product_service import get_product_by_id
from utils.helpers import organize_amazon_search


def get_all_records():
    prices_collection = get_collection("prices")
    prices = prices_collection.find()
    records: list(PriceDTO) = []
    for price in prices:
        product = get_product_by_id(price["product_id"])
        records.append(
            PriceDTO(
                newPrice=price["new_price"],
                oldPrice=price["old_price"],
                discount=price["discount"],
                product_url=product["url"],
                promotion_init_day=price["promotion_initial_date"],
                promotion_final_day=price["promotion_final_date"],
            )
        )
    return records


def get_all_records_from_search_input(store: str):
    try:
        if store == "pcdiga":
            return []
        elif store == "amazon":
            return get_all_searchs_from_amazon()
        else:
            raise Exception("Unknown store")
    except Exception as e:
        raise e


def get_records_from_product_by_store(searched_item: str, store: str):
    try:
        if store == "pcdiga":
            return []
        elif store == "amazon":
            return get_search_item_from_amazon(searched_item)
        else:
            raise Exception("Unknown store")
    except Exception as e:
        raise e


def get_all_searchs_from_amazon():
    try:
        amazon_search_collection = get_collection("amazon_search")
        return [
            SearchProduct(**{k: v for k, v in item.items() if k != "_id"}).to_dict()
            for item in amazon_search_collection.find()
        ]
    except Exception as e:
        raise e


def get_search_item_from_amazon(searched_item: str):
    try:
        amazon_search_collection = get_collection("amazon_search")
        products = [
            SearchProduct(**{k: v for k, v in item.items() if k != "_id"}).to_dict()
            for item in amazon_search_collection.find({"search_product": searched_item})
        ]

        return organize_amazon_search(products)
    except Exception as e:
        raise e


def delete_all_searchs_from_amazon():
    try:
        amazon_search_collection = get_collection("amazon_search")
        amazon_search_collection.delete_many({})
    except Exception as e:
        raise e
