from pydantic import BaseModel


class ProductBody(BaseModel):
    url: str
    store: str

    def to_str(self):
        return f"URL: {self.url}, Store: {self.store}"


class Product(BaseModel):
    uuid: str
    url: str
    store: str

    def to_str(self):
        return f"URL: {self.url}, Store: {self.store}"

    def to_dict(self):
        return {"uuid": self.uuid, "url": self.url, "store": self.store}


class ProductDTO(BaseModel):
    uuid: str
    url: str
    store: str
    product_name: str | None

    def to_dict(self):
        return {"uuid": self.uuid, "url": self.url, "store": self.store, "product_name": self.product_name}
    
    def to_str(self):
        return f"URL: {self.url}, Store: {self.store}, Product: {self.product_name}"

class SearchProduct(BaseModel):
    uuid: str | None
    title: str
    price: str | None
    classification: str
    url: str
    number_reviews: str
    date: str
    
    def to_dict(self):
        return {
            "uuid": self.uuid,
            "title": self.title,
            "price": self.price,
            "classification": self.classification,
            "url": self.url,
            "number_reviews": self.number_reviews,
            "date": self.date
        }