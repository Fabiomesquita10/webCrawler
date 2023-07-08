from pprint import pprint
from models.analytics_model import AnalyticsDTO, AnalyticsRecords, PriceDTO
from models.product_model import SearchProduct
from services.database_service import get_collection
from services.product_service import get_products
from utils.helpers import get_analytics_by_product_uuid, get_records_from_search, organize_amazon_search


def get_all_records_from_search(searched_item: str, store: str):
    try:
        if store == "pcdiga":
            return []
        elif store == "amazon":
            return get_records_from_search_amazon(store, searched_item)
        else:
            raise Exception("Unknown store")
    except Exception as e:
        raise e


def get_records_from_search_amazon(store, searched_item: str):
    try:
        records = []
        
        searched_items = get_records_from_search(store, searched_item) # get the items from the search that i want
        products = get_products("amazon") # get the all the products from amazon
        
        #check all the products from amazon that were found in that search
        matched_products_uuids = {item["uuid"]: item["title"] for item in searched_items if any(item["uuid"] == product.uuid for product in products)}
        
        # get all the analyzed products 
        analytics_collection = get_collection("analytics")
        for product_uuid, product_name in matched_products_uuids.items():
            analytics_data = analytics_collection.find({"product_id": product_uuid})
            records.append(AnalyticsRecords(product_name=product_name, records=[AnalyticsDTO(**analytics) for analytics in analytics_data]).to_dict())
        
        return records   
    except Exception as e:
        raise e


def delete_records():
    try:
        amazon_search_collection = get_collection("analytics")
        amazon_search_collection.delete_many({})
    except Exception as e:
        raise e


def get_product_analytics(product_uuid: str):
    return [
        AnalyticsDTO(**product).to_dict()
        for product in get_analytics_by_product_uuid(product_uuid)
    ]
