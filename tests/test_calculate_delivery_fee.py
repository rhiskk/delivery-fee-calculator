import pytest

from app.calculate_delivery_fee import calculate_delivery_fee
from app.utils import utc_iso_str_to_datetime

MONDAY_1PM = utc_iso_str_to_datetime("2024-01-15T13:00:00Z")


@pytest.mark.parametrize(
    ("delivery_distance", "expected_fee"),
    [
        (1000, 200),
        (1499, 300),
        (1500, 300),
        (1501, 400),
        (5001, 1100),
    ],
)
def test_it_calculates_delivery_distance_fee(delivery_distance: int, expected_fee: int):
    delivery_fee = calculate_delivery_fee(
        cart_value=1000,
        delivery_distance=delivery_distance,
        number_of_items=4,
        time=MONDAY_1PM,
    )
    assert delivery_fee == expected_fee


def test_it_adds_small_order_surcharge():
    delivery_fee = calculate_delivery_fee(
        cart_value=890,
        delivery_distance=1,
        number_of_items=4,
        time=MONDAY_1PM,
    )
    base_plus_small_order_surcharge = 310
    assert delivery_fee == base_plus_small_order_surcharge


@pytest.mark.parametrize(
    ("number_of_items", "expected_fee"),
    [(4, 200), (5, 250), (6, 300), (10, 500), (13, 770)],
)
def test_it_adds_item_amount_surcharge(number_of_items: int, expected_fee: int):
    delivery_fee = calculate_delivery_fee(
        cart_value=1000,
        delivery_distance=1,
        number_of_items=number_of_items,
        time=MONDAY_1PM,
    )
    assert delivery_fee == expected_fee


def test_it_doen_not_exceed_maximum_fee():
    delivery_fee = calculate_delivery_fee(
        cart_value=1000,
        delivery_distance=10000,
        number_of_items=20,
        time=MONDAY_1PM,
    )
    maximum_fee = 1500
    assert delivery_fee == maximum_fee


def test_it_gives_free_delivery_for_orders_over_200_e():
    delivery_fee = calculate_delivery_fee(
        cart_value=20000,
        delivery_distance=10000,
        number_of_items=20,
        time=MONDAY_1PM,
    )
    free = 0
    assert delivery_fee == free


FRIDAY_3PM = utc_iso_str_to_datetime("2024-01-19T15:00:00Z")


def test_it_adds_friday_rush_multiplier_at_3pm():
    delivery_fee = calculate_delivery_fee(
        cart_value=1000,
        delivery_distance=1,
        number_of_items=1,
        time=FRIDAY_3PM,
    )
    base_with_rush_multiplier = 240
    assert delivery_fee == base_with_rush_multiplier


FRIDAY_6_45PM = utc_iso_str_to_datetime("2024-01-19T18:45:00Z")


def test_it_adds_friday_rush_multiplier_at_6_45pm():
    delivery_fee = calculate_delivery_fee(
        cart_value=1000,
        delivery_distance=1,
        number_of_items=1,
        time=FRIDAY_6_45PM,
    )
    base_with_rush_multiplier = 240
    assert delivery_fee == base_with_rush_multiplier


FRIDAY_7PM = utc_iso_str_to_datetime("2024-01-19T19:00:00Z")


def test_it_adds_friday_rush_multiplier_at_7pm():
    delivery_fee = calculate_delivery_fee(
        cart_value=1000,
        delivery_distance=1,
        number_of_items=1,
        time=FRIDAY_7PM,
    )
    base_with_rush_multiplier = 240
    assert delivery_fee == base_with_rush_multiplier


FRIDAY_7_00_01PM = utc_iso_str_to_datetime("2024-01-19T19:00:01Z")


def test_it_does_not_add_friday_rush_multiplier_after_7_pm():
    delivery_fee = calculate_delivery_fee(
        cart_value=1000,
        delivery_distance=1,
        number_of_items=1,
        time=FRIDAY_7_00_01PM,
    )
    base_fee = 200
    assert delivery_fee == base_fee


FRIDAY_2_59_59PM = utc_iso_str_to_datetime("2024-01-19T14:59:59Z")


def test_it_does_not_add_friday_rush_multiplier_before_3_pm():
    delivery_fee = calculate_delivery_fee(
        cart_value=1000,
        delivery_distance=1,
        number_of_items=1,
        time=FRIDAY_2_59_59PM,
    )
    base_fee = 200
    assert delivery_fee == base_fee
