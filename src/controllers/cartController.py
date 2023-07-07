from fastapi import APIRouter

from models.cart_model import cartUpdateBody, cartCreateBody
from services.cart_service import (
    create_cart as _create_cart,
    get_all_carts as _get_all_carts,
    update_cart as _update_cart,
    get_cart_by_uuid as _get_cart_by_uuid,
    get_carts_by_user_uuid as _get_carts_by_user,
    delete_carts_by_uuid as _delete_carts_by_uuid,
    delete_all_carts_from_user as _delete_all_carts_from_user,
    delete_all_carts as _delete_all_carts,
)

cartRouter = APIRouter(prefix="/cart", tags=["Cart"])


@cartRouter.post("")
def create_cart(cart_info: cartCreateBody):
    return _create_cart(cart_info)


@cartRouter.patch("/{cart_uuid}")
def update_cart(cart_info: cartUpdateBody, cart_uuid: str):
    return _update_cart(cart_info, cart_uuid)


@cartRouter.delete("")
def delete_all_carts():
    return _delete_all_carts()


@cartRouter.delete("/{cart_uuid}")
def delete_cart_by_uuid(cart_uuid: str):
    return _delete_carts_by_uuid(cart_uuid)


@cartRouter.delete("/user/{user_uuid}")
def delet_all_carts_from_user(user_uuid: str):
    return _delete_all_carts_from_user(user_uuid)


@cartRouter.get("")
def get_all_carts():
    return _get_all_carts()


@cartRouter.get("/user/{user_uuid}")
def get_carts_by_user_uuid(user_uuid: str):
    return _get_carts_by_user(user_uuid)


@cartRouter.get("/{cart_uuid}")
def get_cart_by_uuid(cart_uuid: str):
    return _get_cart_by_uuid(cart_uuid)
