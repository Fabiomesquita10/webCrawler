import uuid
from aiohttp_retry import List
from models.product_model import ProdcutUpdate, ProductBody, ProductDTO
from services.database_service import get_collection
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
from utils.helpers import (
    check_if_product_exists as _check_if_product_exists,
    check_if_url_exists as _check_if_url_exists,
    get_product_by_uuid as _get_product_by_uuid,
    validate_url as _validate_url,
    get_products as _get_products,
    verif_store_name as _verif_store_name,
)


class ProductException(HTTPException):
    def __init__(self, status_code: status, message: str):
        super().__init__(status_code, detail={"message": message})


def create_product(
    product: ProductBody, given_product_uuid: str = None, product_name: str = None
) -> ProductDTO:
    try:
        if not _validate_url(product.url):
            raise ProductException(
                status_code=status.HTTP_409_CONFLICT, message="Invalid Url!"
            )

        if _check_if_url_exists(product.url):
            raise ProductException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                message="Product already created!",
            )

        if not _verif_store_name(product.store):
            raise ProductException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                message="Invalid store name, please insert insert Pcdiga or Amazon!",
            )

        product_collection = get_collection("products")
        product_uuid = (
            given_product_uuid if given_product_uuid != None else str(uuid.uuid4())
        )

        data = {
            "uuid": product_uuid,
            "store": product.store,
            "url": product.url,
            "product_name": product_name,
        }

        if _check_if_product_exists(product_uuid):
            raise ProductException(
                status_code=status.HTTP_409_CONFLICT, message="Product already exists!"
            )

        product_collection.insert_one(data)

        return JSONResponse(
            content=ProductDTO(**data).to_dict(),
            status_code=status.HTTP_201_CREATED,
        )
    except ProductException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Internal server error: {e}"},
        )


def get_product_by_uuid(product_uuid: str) -> ProductDTO:
    try:
        if not _check_if_product_exists(product_uuid):
            raise ProductException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                message="ProductUuid not valid! Product not found!",
            )
        return JSONResponse(
            content=ProductDTO(**_get_product_by_uuid(product_uuid)).to_dict(),
            status_code=status.HTTP_200_OK,
        )
    except ProductException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Internal server error.\n{e}"},
        )


def get_products(
    store: str = None, page: int = 1, page_size: int = 10
) -> List[ProductDTO]:
    try:
        if store and not _verif_store_name(store):
            raise ProductException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                message="Invalid store name, please insert Pcdiga or Amazon!",
            )

        products = _get_products(store) if store else _get_products()

        # Calculate the start and end index based on the page and page_size
        start_index = (page - 1) * page_size
        end_index = start_index + page_size

        # Get the products for the current page
        paginated_products = products[start_index:end_index]

        return JSONResponse(
            content=[product.to_dict() for product in paginated_products],
            status_code=status.HTTP_201_CREATED,
        )
    except ProductException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Internal server error: {e}"},
        )


def delete_product_by_uuid(product_uuid: str) -> JSONResponse:
    try:
        if not _check_if_product_exists(product_uuid):
            raise ProductException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                message="ProductUuid not valid! Product not found!",
            )
        product_collection = get_collection("products")

        result = product_collection.delete_one({"uuid": product_uuid})

        if result.deleted_count > 0:
            return JSONResponse(
                content={"message": "Product deleted successfully"},
                status_code=status.HTTP_202_ACCEPTED,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": "Internal error deleting the product"},
            )
    except ProductException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Internal server error.\n{e}"},
        )


def delete_products() -> JSONResponse:
    try:
        product_collection = get_collection("products")

        result = product_collection.delete_many({})

        if result.deleted_count > 0:
            return JSONResponse(
                content={"message": "All products were deleted successfully"},
                status_code=status.HTTP_202_ACCEPTED,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": "Internal error deleting the product"},
            )
    except ProductException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Internal server error.\n{e}"},
        )


def delete_all_products_from_store(store_name):
    try:
        if not _verif_store_name(store_name):
            raise ProductException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                message="Invalid store name, please insert insert Pcdiga or Amazon!",
            )
        product_collection = get_collection("products")
        result = product_collection.delete_many({"store": store_name})
        if result.deleted_count > 0:
            return JSONResponse(
                content={
                    "message": f"All products from {store_name} deleted successfully"
                },
                status_code=status.HTTP_202_ACCEPTED,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": "Internal error deleting the product"},
            )
    except ProductException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Internal server error.\n{e}"},
        )


def update_product(product: ProdcutUpdate, product_uuid: str):
    try:
        product_collection = get_collection("products")
        if not _check_if_product_exists(product_uuid):
            raise ProductException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                message="ProductUuid not valid! Product not found!",
            )
        if product.store and not _verif_store_name(product.store):
            raise ProductException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                message="Invalid store name, please insert insert Pcdiga or Amazon!",
            )
        if product.url and not _validate_url(product.url):
            raise ProductException(
                status_code=status.HTTP_409_CONFLICT, message="Invalid Url!"
            )

        product_to_update = ProductDTO(**_get_product_by_uuid(product_uuid))

        updated_product = {
            "product_name": product.product_name
            if product.product_name
            else product_to_update.product_name,
            "url": product.url if product.url else product_to_update.url,
            "store": product.store if product.store else product_to_update.store,
        }

        product_collection.update_one({"uuid": product_uuid}, {"$set": updated_product})

        updated_product = _get_product_by_uuid(product_uuid)

        return JSONResponse(
            content=ProductDTO(**_get_product_by_uuid(product_uuid)).to_dict(),
            status_code=status.HTTP_201_CREATED,
        )

    except ProductException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Internal server error.\n{e}"},
        )
