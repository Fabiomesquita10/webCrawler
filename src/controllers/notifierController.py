from fastapi import APIRouter
from services.notifier_service import (
    get_product_analytics as _get_product_analytics,
)

notifierRouter = APIRouter(prefix="/discordNotifier", tags=["Notifier"])

@notifierRouter.post("/product/{product_id}")
def get_product_analytics(product_uuid: str):
    return _get_product_analytics(product_uuid)
