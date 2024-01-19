from app.calculator import calculate_delivery_fee
from app.calculator import Order


def test_small_order_surcharge():
    time = "2024-01-15T13:00:00Z"
    order: Order = {
        "cart_value": 1000,
        "delivery_distance": 1000,
        "number_of_items": 1,
        "time": time,
    }
    assert calculate_delivery_fee(order) == 310
