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
