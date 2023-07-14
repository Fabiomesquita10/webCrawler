from pydantic import BaseModel
import uuid
from typing import List
from models.product_model import Product, ProductDTO

from utils.helpers import get_product_by_uuid as _get_product_by_uuid


class cartCreateBody(BaseModel):
    product_uuid: str
    user_uuid: str


class cartUpdateBody(BaseModel):
    product_uuid: str
    operation: str


class Cart(BaseModel):
    uuid: str
    product_uuid: List[str]
    user_uuid: str

    def get_cart_info(self):
        products = [
            ProductDTO(**_get_product_by_uuid(product_uuid)).to_dict()
            for product_uuid in self.product_uuid
        ]
        return {
            "user_uuid": self.user_uuid,
            "cart_uuid": self.uuid,
            "products": products,
        }

    def get_all_products_uuids(self):
        return [
            {
                ProductDTO(**_get_product_by_uuid(product_uuid))
                .to_dict()["store"]: ProductDTO(**_get_product_by_uuid(product_uuid))
                .to_dict()["uuid"]
            }
            for product_uuid in self.product_uuid
        ]
