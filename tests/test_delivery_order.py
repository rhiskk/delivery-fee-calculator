import pytest
from app.delivery_order import DeliveryOrder


# Tests for input validation
def test_accepts_valid_inputs():
    order = DeliveryOrder(
        cart_value=790,
        delivery_distance=2235,
        number_of_items=4,
        time="2024-01-15T13:00:00Z",
    )
    assert isinstance(order, DeliveryOrder)


@pytest.mark.parametrize(
    "_description, cart_value, delivery_distance, number_of_items, time",
    [
        ("Negative cart value", -1, 2235, 4, "2024-01-15T13:00:00Z"),
        ("Negative delivery distance", 790, -1, 4, "2024-01-15T13:00:00Z"),
        ("Negative number of items", 790, 2235, -1, "2024-01-15T13:00:00Z"),
        ("Invalid time format", 790, 2235, 4, "2024-01-15 13:00:00Z"),
        ("Invalid time format", 790, 2235, 4, "2024-01-15T13:00:00"),
    ],
    ids=lambda _description: _description,
)
def test_rejects_invalid_inputs(
    _description, cart_value, delivery_distance, number_of_items, time
):
    with pytest.raises(ValueError):
        DeliveryOrder(
            cart_value=cart_value,
            delivery_distance=delivery_distance,
            number_of_items=number_of_items,
            time=time,
        )


# Tests for delivery fee calculation
@pytest.mark.parametrize(
    "delivery_distance, expected_fee",
    [
        (1000, 200),
        (1499, 300),
        (1500, 300),
        (1501, 400),
        (5001, 1100),
    ],
)
def test_delivery_distance_fee(delivery_distance, expected_fee):
    delivery_order = DeliveryOrder(
        cart_value=1000,
        delivery_distance=delivery_distance,
        number_of_items=4,
        time="2024-01-15T13:00:00Z",
    )
    assert delivery_order.delivery_fee == expected_fee


def test_adds_small_order_surcharge():
    delivery_order = DeliveryOrder(
        cart_value=890,
        delivery_distance=1,
        number_of_items=4,
        time="2024-01-15T13:00:00Z",
    )
    assert delivery_order.delivery_fee == 310


def test_does_not_add_small_order_surcharge():
    delivery_order = DeliveryOrder(
        cart_value=1000,
        delivery_distance=1,
        number_of_items=4,
        time="2024-01-15T13:00:00Z",
    )
    assert delivery_order.delivery_fee == 200


@pytest.mark.parametrize(
    "number_of_items, expected_fee",
    [(4, 200), (5, 250), (6, 300), (10, 500), (13, 770)],
)
def test_item_amount_surcharge(number_of_items, expected_fee):
    delivery_order = DeliveryOrder(
        cart_value=1000,
        delivery_distance=1,
        number_of_items=number_of_items,
        time="2024-01-15T13:00:00Z",
    )
    assert delivery_order.delivery_fee == expected_fee


def test_maximum_fee():
    delivery_order = DeliveryOrder(
        cart_value=1000,
        delivery_distance=10000,
        number_of_items=20,
        time="2024-01-15T13:00:00Z",
    )
    assert delivery_order.delivery_fee == 1500
