import uuid
from models.user_model import User, userBody
from services.database_service import get_collection
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status


def create_user(user_data: userBody) -> dict:
    try:
        user_collection = get_collection("users")
        user_uuid = str(uuid.uuid4())
        new_user = {"uuid": user_uuid, "username": user_data.username}

        existing_user = user_collection.find_one({"username": user_data.username})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": "User already exists in the database",
                    "id": existing_user["uuid"],
                },
            )
        user_collection.insert_one(new_user)
        return {
            "message": "User created successfully",
            "uuid": user_uuid,
        }
    except Exception as e:
        raise e


def get_user_by_uuid(user_uuid: str) -> User | Exception:
    try:
        user_collection = get_collection("users")
        existing_user = user_collection.find_one({"uuid": user_uuid})
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail={
                    "message": "Uuid not valid! User not found!",
                },
            )

        user = User(
            **{
                "uuid": existing_user["uuid"],
                "username": existing_user["username"],
            }
        ).dict()
        return JSONResponse(content=user, status_code=status.HTTP_200_OK)

    except Exception as e:
        raise e


def get_all_users() -> list[User]:
    try:
        user_collection = get_collection("users")
        users = user_collection.find()
        all_users = [
            User(
                **{
                    "uuid": user["uuid"],
                    "username": user["username"],
                }
            ).dict()
            for user in users
        ]
        return JSONResponse(content=all_users, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise e


def update_user_by_uuid(user_uuid: str, user_data: userBody) -> dict:
    try:
        updated_user = {"uuid": user_uuid, "username": user_data.username}
        user_collection = get_collection("users")

        if user_collection.find_one({"uuid": user_uuid}):
            result = user_collection.update_one(
                {"uuid": user_uuid}, {"$set": updated_user}
            )

            if result.modified_count > 0:
                content = User(**updated_user).dict()
                return JSONResponse(content=content, status_code=status.HTTP_200_OK)
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail="User already with this update!",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
    except Exception as e:
        raise e


def delete_user_by_uuid(user_uuid: str) -> dict:
    try:
        user_collection = get_collection("users")

        # Find the user with the specified UUID
        user = user_collection.find_one({"uuid": user_uuid})
        if user:
            # Delete the user from the collection
            result = user_collection.delete_one({"uuid": user_uuid})

            if result.deleted_count > 0:
                return {"message": "User deleted successfully"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_412_PRECONDITION_FAILED,
                    detail="User deletion failed, by unknown reason. Can't delete the user!",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail="User deletion failed, because there is no user with the specified UUID!",
            )
    except Exception as e:
        raise e


def delete_all_users() -> dict:
    try:
        user_collection = get_collection("users")

        result = user_collection.delete_many({})

        if result.deleted_count > 0:
            return JSONResponse(
                content={"message": "All users deleted successfully"},
                status_code=status.HTTP_202_ACCEPTED,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"message": "No users found to delete"},
            )
    except Exception as e:
        raise e
