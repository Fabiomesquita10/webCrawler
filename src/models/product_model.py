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
