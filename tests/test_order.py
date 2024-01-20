import pytest
from app.order import Order


def test_accepts_valid_input_types():
    order = Order(
        cart_value=790,
        delivery_distance=2235,
        number_of_items=4,
        time="2024-01-15T13:00:00Z",
    )
    assert isinstance(order, Order)


def test_rejects_negative_cart_value():
    with pytest.raises(ValueError):
        Order(
            cart_value=-1,
            delivery_distance=2235,
            number_of_items=4,
            time="2024-01-15T13:00:00Z",
        )


def test_rejects_negative_delivery_distance():
    with pytest.raises(ValueError):
        Order(
            cart_value=790,
            delivery_distance=-1,
            number_of_items=4,
            time="2024-01-15T13:00:00Z",
        )


def test_rejects_negative_number_of_items():
    with pytest.raises(ValueError):
        Order(
            cart_value=790,
            delivery_distance=2235,
            number_of_items=-1,
            time="2024-01-15T13:00:00Z",
        )


def test_rejects_invalid_time():
    with pytest.raises(ValueError):
        Order(
            cart_value=790,
            delivery_distance=2235,
            number_of_items=4,
            time="2024-01-15 13:00:00",
        )
