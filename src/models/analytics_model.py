from typing import List
from pydantic import BaseModel


class Price(BaseModel):
    newPrice: float
    oldPrice: float
    discount: float | None

    def to_str(self):
        return f"Current Price: {self.newPrice} €\nProduct Price: {self.oldPrice} €\nDiscount: {self.discount} €"


class PriceDTO(BaseModel):
    newPrice: float
    oldPrice: float
    discount: float
    product_url: str
    promotion_init_day: str | None
    promotion_final_day: str | None


class AnalyticsDTO(BaseModel):
    product_id: str
    new_price: float
    old_price: float
    discount: float

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "new_price": self.new_price,
            "old_price": self.old_price,
            "discount": self.discount,
        }

    def get_price_dict(self):
        return Price(newPrice=self.new_price, oldPrice=self.old_price, discount=self.discount)


class AnalyticsRecords(BaseModel):
    product_name: str
    records: List[AnalyticsDTO]

    def to_dict(self):
        return {
            "product_name": self.product_name,
            "records": [record.to_dict() for record in self.records],
        }
