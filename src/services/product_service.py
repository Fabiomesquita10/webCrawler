from urllib.parse import urlparse
from models.product_model import Product, ProductBody, ProductDTO
from services.database_service import get_collection
import uuid

def create_product(url_data: ProductBody) -> dict:
    try:
        url_collection = get_collection("products")
        product_uuid = str(uuid.uuid4())
        data = {
            "uuid": product_uuid,
            "store": url_data.store,
            "url": url_data.url,
            "product_name": None,
        }

        existing_url = url_collection.find_one({"url": url_data.url})
        if existing_url:
            return {
                "message": "URL already exists in the database",
                "id": existing_url["url"],
            }

        parsed_url = urlparse(url_data.url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            print("Invalid URL")  # Log the invalid URL
            return {"message": "Invalid URL"}

        url_collection.insert_one(data)
        print("Inserted data UUID:", product_uuid)  # Log the inserted data ID
        return {"message": "Product added successfully", "uuid": product_uuid}
    except Exception as e:
        print("Error:", e)  # Log the error message
        raise Exception("Can't add new URL: " + str(e))


def get_products():
    url_collection = get_collection("products")
    urls = url_collection.find()
    return [
        ProductDTO(
            **{
                "uuid": url["uuid"],
                "url": url["url"],
                "store": url["store"],
                "product_name": url.get("product_name") or None,
            }
        )
        for url in urls
    ]


def delete_products() -> dict:
    try:
        url_collection = get_collection("products")
        
        # Delete all documents in the "products" collection
        result = url_collection.delete_many({})
        
        if result.deleted_count > 0:
            return {"message": "All products deleted successfully"}
        else:
            return {"message": "No products found to delete"}
    except Exception as e:
        raise Exception("Can't delete products: " + str(e))



def delete_product_by_uuid(product_uuid: str) -> dict:
    try:
        url_collection = get_collection("products")
        
        # Find the product with the specified UUID
        product = url_collection.find_one({"uuid": product_uuid})
        
        if product:
            # Delete the product from the collection
            result = url_collection.delete_one({"uuid": product_uuid})
            
            if result.deleted_count > 0:
                return {"message": "Product deleted successfully"}
            else:
                return {"message": "Product deletion failed"}
        else:
            return {"message": "Product not found"}
    except Exception as e:
        raise Exception("Can't delete product: " + str(e))


def update_product(url: Product, product_name: str):
    url_collection = get_collection("products")
    updated_data = {"store": url.store, "url": url.url, "product_name": product_name}
    url_collection.update_one({"url": url.url}, {"$set": updated_data})


def get_product_by_url(url: str):
    url_collection = get_collection("products")
    product = url_collection.find_one({"url": url})
    return product

def get_product_by_uuid(product_uuid: str):
    url_collection = get_collection("products")
    product = url_collection.find_one({"uuid": product_uuid})
    return product

def get_product_by_id(id: str):
    url_collection = get_collection("products")
    product = url_collection.find_one({"_id": id})
    return product
