import pytest
from app.calculate_delivery_fee import calculate_delivery_fee
from datetime import datetime

MONDAY_1PM = datetime.fromisoformat("2024-01-15T13:00:00Z")
FRIDAY_3PM = datetime.fromisoformat("2024-01-19T15:00:00Z")
FRIDAY_6_45PM = datetime.fromisoformat("2024-01-19T18:45:00Z")
FRIDAY_7PM = datetime.fromisoformat("2024-01-19T19:00:00Z")


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
def test_calculates_delivery_distance_fee(delivery_distance: int, expected_fee: int):
    delivery_fee = calculate_delivery_fee(
        cart_value=1000,
        delivery_distance=delivery_distance,
        number_of_items=4,
        time=MONDAY_1PM,
    )
    assert delivery_fee == expected_fee


def test_adds_small_order_surcharge():
    delivery_fee = calculate_delivery_fee(
        cart_value=890,
        delivery_distance=1,
        number_of_items=4,
        time=MONDAY_1PM,
    )
    assert delivery_fee == 310


@pytest.mark.parametrize(
    "number_of_items, expected_fee",
    [(4, 200), (5, 250), (6, 300), (10, 500), (13, 770)],
)
def test_adds_item_amount_surcharge(number_of_items: int, expected_fee: int):
    delivery_fee = calculate_delivery_fee(
        cart_value=1000,
        delivery_distance=1,
        number_of_items=number_of_items,
        time=MONDAY_1PM,
    )
    assert delivery_fee == expected_fee


def test_maximum_fee():
    delivery_fee = calculate_delivery_fee(
        cart_value=1000,
        delivery_distance=10000,
        number_of_items=20,
        time=MONDAY_1PM,
    )
    assert delivery_fee == 1500


def test_free_delivery_for_orders_over_200_e():
    delivery_fee = calculate_delivery_fee(
        cart_value=20000,
        delivery_distance=10000,
        number_of_items=20,
        time=MONDAY_1PM,
    )
    assert delivery_fee == 0


def test_adds_friday_rush_multiplier_3PM():
    delivery_fee = calculate_delivery_fee(
        cart_value=1000,
        delivery_distance=1,
        number_of_items=1,
        time=FRIDAY_3PM,
    )
    assert delivery_fee == 240


def test_adds_friday_rush_multiplier_6_45PM():
    delivery_fee = calculate_delivery_fee(
        cart_value=1000,
        delivery_distance=1,
        number_of_items=1,
        time=FRIDAY_6_45PM,
    )
    assert delivery_fee == 240


def test_does_not_add_friday_rush_multiplier_7PM():
    delivery_fee = calculate_delivery_fee(
        cart_value=1000,
        delivery_distance=1,
        number_of_items=1,
        time=FRIDAY_7PM,
    )
    assert delivery_fee == 200
