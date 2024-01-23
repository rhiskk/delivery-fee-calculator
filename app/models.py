from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictInt,
    field_validator,
)


def utc_iso_str_to_datetime(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")


class DeliveryFeeRequest(BaseModel):
    """Delivery fee request model.

    Attributes:
        cart_value (int): Value of the shopping cart in cents.
        delivery_distance (int): The distance between the store and
            customer's location in meters.
        number_of_items (int): The number of items in the
            customer's shopping cart.
        time (datetime): Order time in UTC in ISO format
            (YYYY-MM-DDTHH:MM:SSZ).
    """

    cart_value: StrictInt = Field(
        ..., ge=0, description="Value of the shopping cart in cents."
    )
    delivery_distance: StrictInt = Field(
        ...,
        ge=0,
        description=(
            "The distance between the store and "
            "customer's location in meters."
        ),
    )
    number_of_items: StrictInt = Field(
        ...,
        ge=0,
        description="The number of items in the customer's shopping cart.",
    )
    time: str = Field(
        ...,
        description="Order time in UTC in ISO format (YYYY-MM-DDTHH:MM:SSZ).",
    )

    @field_validator("time")
    def validate_time(cls, value: str):
        try:
            utc_iso_str_to_datetime(value)
        except ValueError as err:
            raise ValueError(
                "time must be a date in UTC in ISO format"
                "(YYYY-MM-DDTHH:MM:SSZ)"
            ) from err
        return value

    # Example values for OpenAPI documentation
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "cart_value": 790,
                "delivery_distance": 2235,
                "number_of_items": 4,
                "time": "2024-01-15T13:00:00Z",
            }
        }
    )


class DeliveryFeeResponse(BaseModel):
    """
    Delivery fee response model.

    Attributes:
        delivery_fee (int): Calculated delivery fee in cents.
    """

    delivery_fee: StrictInt = Field(
        ..., ge=0, description="Calculated delivery fee in cents."
    )

    # Example values for OpenAPI documentation
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "delivery_fee": 710,
            }
        }
    )
