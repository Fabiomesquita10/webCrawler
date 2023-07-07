import uuid
from models.cart_model import Cart, cartCreateBody, cartUpdateBody
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
from services.database_service import get_collection

from utils.helpers import (
    check_if_cart_exists,
    check_if_product_exists,
    check_if_cart_exists,
    check_if_user_exists,
    check_product_in_cart,
    validate_update_cart_op,
)


class CartException(HTTPException):
    def __init__(self, status_code: status, message: str):
        super().__init__(status_code, detail={"message": message})


def create_cart(cart_info: cartCreateBody) -> JSONResponse:
    try:
        if not check_if_product_exists(cart_info.product_uuid):
            raise CartException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                message="ProductUuid not valid! Product not found!",
            )
        if not check_if_user_exists(cart_info.user_uuid):
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                message="userUuid not valid! User not found!",
            )
        cart_uuid = str(uuid.uuid4())
        new_cart = {
            "uuid": cart_uuid,
            "product_uuid": [cart_info.product_uuid],
            "user_uuid": cart_info.user_uuid,
        }

        cart_collection = get_collection("carts")
        cart_collection.insert_one(new_cart)

        return JSONResponse(
            content=Cart(**new_cart).get_cart_info(),
            status_code=status.HTTP_201_CREATED,
        )

    except CartException as e:
        raise e

    except Exception as e:
        # Handle other exceptions or log the error for debugging purposes
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error."},
        )


def update_cart(cart_info: cartUpdateBody, cart_uuid: str) -> JSONResponse:
    try:
        if not validate_update_cart_op(cart_info.operation):
            raise CartException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                message="Invalid operation! Please provide 'add' or 'remove'.",
            )
        if not check_if_cart_exists(cart_uuid):
            raise CartException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                message="Cart_uuid not valid! Cart not found!",
            )
        if not check_if_product_exists(cart_info.product_uuid):
            raise CartException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                message="Product_uuid not valid! Product not found!",
            )

        cart_collection = get_collection("carts")
        cart = cart_collection.find_one({"uuid": cart_uuid})
        cart_product_list = cart["product_uuid"]

        if cart_info.operation == "add":
            if check_product_in_cart(cart_product_list, cart_info.product_uuid):
                raise CartException(
                    status_code=status.HTTP_409_CONFLICT,
                    message="This product has already been added!",
                )

            cart_product_list.append(cart_info.product_uuid)

        if cart_info.operation == "remove":
            if not check_product_in_cart(cart_product_list, cart_info.product_uuid):
                raise CartException(
                    status_code=status.HTTP_409_CONFLICT,
                    message="This product is not in the cart!",
                )
            cart_product_list.remove(cart_info.product_uuid)

        cart["product_uuid"] = cart_product_list
        result = cart_collection.update_one({"uuid": cart_uuid}, {"$set": cart})
        if result.modified_count > 0:
            content = Cart(**cart).get_cart_info()
            return JSONResponse(content=content, status_code=status.HTTP_202_ACCEPTED)

    except CartException as e:
        raise e


def delete_all_carts() -> JSONResponse:
    try:
        cart_collection = get_collection("carts")
        cart_collection.delete_many({})
    except Exception as e:
        raise e


def delete_carts_by_uuid(cart_uuid: str) -> JSONResponse:
    try:
        cart_collection = get_collection("carts")

        if not check_if_cart_exists(cart_uuid):
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail={
                    "message": "Uuid not valid! Cart not found!",
                },
            )
        # Find the cart with the specified UUID
        cart = cart_collection.find_one({"uuid": cart_uuid})
        if cart:
            # Delete the cart from the collection
            result = cart_collection.delete_one({"uuid": cart_uuid})

            if result.deleted_count > 0:
                return {"message": "Cart deleted successfully"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_412_PRECONDITION_FAILED,
                    detail="Cart deletion failed, by unknown reason. Can't delete the cart!",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail="cart deletion failed, because there is no cart with the specified UUID!",
            )
    except Exception as e:
        raise e


def delete_all_carts_from_user(user_uuid: str) -> JSONResponse:
    try:
        cart_collection = get_collection("carts")

        if not check_if_user_exists(user_uuid):
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail={
                    "message": "Uuid not valid! User not found!",
                },
            )
        # Find the cart with the specified UUID
        cart = cart_collection.find_one({"user_uuid": user_uuid})
        if cart:
            # Delete the cart from the collection
            result = cart_collection.delete_many({"user_uuid": user_uuid})

            if result.deleted_count > 0:
                return {
                    "message": f"Cart from user: {user_uuid} were deleted successfully"
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_412_PRECONDITION_FAILED,
                    detail="Cart deletion failed, by unknown reason. Can't delete the cart!",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail="cart deletion failed, because there is no cart with the specified UUID!",
            )
    except Exception as e:
        raise e


def get_all_carts() -> JSONResponse:
    try:
        cart_collection = get_collection("carts")
        carts = cart_collection.find({})
        return JSONResponse(
            content=[Cart(**cart).get_cart_info() for cart in carts],
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise e


def get_carts_by_user_uuid(user_uuid: str) -> JSONResponse:
    try:
        if not check_if_user_exists(user_uuid):
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                message="UserUuid not valid! User not found!",
            )

        cart_collection = get_collection("carts")

        existing_cart = cart_collection.find({"user_uuid": user_uuid})

        if not existing_cart:
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail={
                    "message": "Uuid not valid! Cart not found!",
                },
            )

        carts = [
            Cart(
                **{
                    "uuid": cart["uuid"],
                    "user_uuid": cart["user_uuid"],
                    "product_uuid": cart["product_uuid"],
                }
            ).get_cart_info()
            for cart in existing_cart
        ]
        return JSONResponse(content=carts, status_code=status.HTTP_200_OK)

    except Exception as e:
        raise e


def get_cart_by_uuid(cart_uuid: str) -> JSONResponse:
    try:
        cart_collection = get_collection("carts")
        if not check_if_cart_exists(cart_uuid):
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail={
                    "message": "Uuid not valid! Cart not found!",
                },
            )

        existing_cart = cart_collection.find_one({"uuid": cart_uuid})
        cart = Cart(
            **{
                "uuid": existing_cart["uuid"],
                "cart_uuid": existing_cart["cart_uuid"],
                "product_uuid": existing_cart["product_uuid"],
            }
        ).get_cart_info()
        return JSONResponse(content=cart, status_code=status.HTTP_200_OK)

    except Exception as e:
        raise e
