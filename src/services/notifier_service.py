from fastapi import HTTPException, status
from models.analytics_model import AnalyticsDTO, Price
from services.message_service import message_builder, send_message
from services.analytics_service import get_product_analytics as _get_product_analytics
from utils.helpers import (
    check_if_product_exists as _check_if_product_exists,
    get_product_by_uuid as _get_product_by_uuid,
)
from fastapi.responses import JSONResponse


class NotifierException(HTTPException):
    def __init__(self, status_code: status, message: str):
        super().__init__(status_code, detail={"message": message})


def get_product_analytics(product_uuid: str) -> JSONResponse:
    try:
        if not _check_if_product_exists(product_uuid):
            raise NotifierException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                message="ProductUuid not valid! Product not found!",
            )
        product = _get_product_by_uuid(product_uuid)

        print(product)

        analytics = _get_product_analytics(product_uuid)
        if len(analytics) == 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                message=f"There is no analytics for product {product_uuid}",
            )

        analytics = AnalyticsDTO(**analytics[::-1][0])
        message = message_builder(
            product_name=product["product_name"],
            url=product["url"],
            prices=analytics.get_price_dict(),
        )

        send_message(message_content=message, tag=True, date=True)

        return JSONResponse(
            content={"message": f"Message: {message} Was sent with success!"},
            status_code=status.HTTP_200_OK,
        )

    except NotifierException as e:
        raise e

    except Exception as e:
        # Handle other exceptions or log the error for debugging purposes
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": f"Internal server error: {e}"},
        )
