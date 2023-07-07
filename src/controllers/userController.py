from fastapi import APIRouter

from models.user_model import userBody
from services.user_service import (
    create_user as _create_user,
    get_user_by_uuid as _get_user_by_uuid,
    get_all_users as _get_all_users,
    update_user_by_uuid as _update_user_by_uuid,
    delete_user_by_uuid as _delete_user_by_uuid,
    delete_all_users as _delete_all_users,
)

userRouter = APIRouter(prefix="/user", tags=["User"])


@userRouter.post("")
def create_user(user_data: userBody):
    return _create_user(user_data)


@userRouter.get("/{user_uuid}")
def get_user_by_uuid(user_uuid: str):
    return _get_user_by_uuid(user_uuid)


@userRouter.get("")
def get_all_users():
    return _get_all_users()


@userRouter.patch("/{user_uuid}")
def update_user_by_uuid(user_uuid: str, user_data: userBody):
    return _update_user_by_uuid(user_uuid, user_data)


@userRouter.delete("/{user_uuid}")
def delete_users_by_uuid(user_uuid: str):
    return _delete_user_by_uuid(user_uuid)


@userRouter.delete("")
def delete_all_users():
    return _delete_all_users()
