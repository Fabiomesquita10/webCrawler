from pprint import pprint
from models.product_model import SearchProduct
from services.database_service import get_collection


def check_if_product_exists(product_uuid: str) -> bool:
    product_collection = get_collection("products")
    return True if product_collection.find_one({"uuid": product_uuid}) else False


def check_if_user_exists(user_uuid: str) -> bool:
    user_collection = get_collection("users")
    return True if user_collection.find_one({"uuid": user_uuid}) else False


def check_if_cart_exists(cart_uuid: str) -> bool:
    cart_collection = get_collection("carts")
    return True if cart_collection.find_one({"uuid": cart_uuid}) else False


def validate_update_cart_op(operation: str) -> bool:
    return operation == "add" or operation == "remove"


def check_product_in_cart(product_list: list, product_uuid: str) -> bool:
    return product_uuid in product_list


def check_if_product_exist_by_name(product_name: str) -> bool:
    product_collection = get_collection("products")
    return (
        True if product_collection.find_one({"product_name": product_name}) else False
    )


def organize_amazon_search(products_list: list) -> list:
    titles = set(product["title"] for product in products_list)
    products = dict()
    for title in titles:
        products[title] = {"searchs": [], "count": 0, "price_avg": 0}

    for product in products_list:
        searched_product = SearchProduct(**product)
        products[searched_product.title]["searchs"].append(
            {
                "price": searched_product.price,
                "url": "https://www.amazon.es" + searched_product.url,
                "classification": searched_product.classification,
            }
        )
        products[searched_product.title]["count"] += 1

    return products


def save_search(scrapped_data: dict):
    analytics_collection = get_collection("analytics")
    for data in scrapped_data:
        product = get_product_by_url(data["url"])
        print(product)
        new_data = {
            "product_id": product["uuid"],
            "new_price": data["prices"].newPrice,
            "old_price": data["prices"].oldPrice,
            "discount": data["prices"].discount,
            "promotion_initial_date": data["promotion_data"][0]
            if data["promotion_data"] is not None
            else None,
            "promotion_final_date": data["promotion_data"][1]
            if data["promotion_data"] is not None
            else None,
        }
        analytics_collection.insert_one(new_data)

def get_product_by_url(url: str):
    url_collection = get_collection("products")
    product = url_collection.find_one({"url": url})
    return product
