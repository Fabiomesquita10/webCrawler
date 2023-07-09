from fastapi import HTTPException, status
from models.analytics_model import AnalyticsDTO, Price
from services.message_service import message_builder, send_message
from services.product_service import get_product_by_uuid
from services.analytics_service import get_product_analytics as _get_product_analytics
from utils.helpers import check_if_product_exists
from fastapi.responses import JSONResponse


def get_product_analytics(product_uuid: str) -> JSONResponse:
    try:
        if not check_if_product_exists(product_uuid):
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                message="ProductUuid not valid! Product not found!",
            )
        product = get_product_by_uuid(product_uuid)

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
            content={"message": f"Message:\n {message}\nWas sent with success!"},
            status_code=status.HTTP_200_OK,
        )
    except HTTPException as e:
        raise e
