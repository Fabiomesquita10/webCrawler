from models.price_model import PriceDTO
from services.database_service import get_collection
from services.product_service import get_product_by_id, get_product_by_url


def clear_prices_record():
    price_collection = get_collection("prices")
    price_collection.delete_many({})


def save_record(scrapped_data: dict):
    prices_collection = get_collection("prices")
    for data in scrapped_data:
        product = get_product_by_url(data["url"])
        new_data = {
            "product_id": product["_id"],
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
        prices_collection.insert_one(new_data)


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
