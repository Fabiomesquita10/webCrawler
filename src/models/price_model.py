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