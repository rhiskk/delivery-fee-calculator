import math
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

BASE_DISTANCE = 1000
BASE_FEE = 200
DISTANCE_UNIT = 500
ADDITIONAL_DISTANCE_FEE = 100
SMALL_ORDER_THRESHOLD = 1000
ITEM_SURCHARGE_THRESHOLD = 4
ITEM_SURCHARGE = 50
BULK_THRESHOLD = 12
BULK_FEE = 120
MAXIMUM_FEE = 1500


class DeliveryOrder(BaseModel):
    cart_value: int = Field(..., ge=0)
    delivery_distance: int = Field(..., ge=0)
    number_of_items: int = Field(..., ge=0)
    time: str

    @field_validator("time")
    def validate_time(cls, value):
        try:
            return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            raise ValueError(
                "time must be a date in UTC in ISO format (YYYY-MM-DDTHH:MM:SSZ)"
            )

    @property
    def delivery_fee(self):
        fee = 0
        fee += self._get_fee()
        fee += self._get_small_order_surcharge()
        fee += self._get_item_surcharge()
        return min(fee, MAXIMUM_FEE)

    def _get_small_order_surcharge(self):
        return max(0, SMALL_ORDER_THRESHOLD - self.cart_value)

    def _get_fee(self):
        base_fee = BASE_FEE
        additional_distance = self.delivery_distance - BASE_DISTANCE
        if additional_distance > 0:
            base_fee += (
                math.ceil(additional_distance / DISTANCE_UNIT) * ADDITIONAL_DISTANCE_FEE
            )
        return base_fee

    def _get_item_surcharge(self):
        fee = 0
        if self.number_of_items > BULK_THRESHOLD:
            fee += BULK_FEE
        fee += max(0, self.number_of_items - ITEM_SURCHARGE_THRESHOLD) * ITEM_SURCHARGE
        return fee
