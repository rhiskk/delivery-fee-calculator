from fastapi import FastAPI

from app.calculate_delivery_fee import calculate_delivery_fee
from app.models import (
    DeliveryFeeRequest,
    DeliveryFeeResponse,
    utc_iso_str_to_datetime,
)

app = FastAPI(title="Delivery Fee Calculator API", version="1.0.0")


@app.post("/calculate_delivery_fee", response_model=DeliveryFeeResponse)
def calculate_delivery_fee_route(request: DeliveryFeeRequest):
    delivery_fee = calculate_delivery_fee(
        request.cart_value,
        request.delivery_distance,
        request.number_of_items,
        utc_iso_str_to_datetime(request.time),
    )
    return DeliveryFeeResponse(delivery_fee=delivery_fee)
