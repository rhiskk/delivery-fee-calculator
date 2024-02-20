import math
from calendar import FRIDAY
from datetime import datetime, time

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
FREE_DELIVERY_THRESHOLD = 20000
FRIDAY_RUSH_START = 15
FRIDAY_RUSH_END = 19
FRIDAY_RUSH_MULTIPLIER = 1.2


def calculate_delivery_fee(
    cart_value: int,
    delivery_distance: int,
    number_of_items: int,
    time: datetime,
) -> int:
    """
    Calculate the delivery fee based on cart value, delivery distance,
    number of items and time.

    Parameters:
    cart_value (int): Value of the shopping cart in cents.
    delivery_distance (int): The distance between the store and customer's
    location in meters.
    number_of_items (int): The number of items in the customer's shopping cart.
    time (datetime): Order time in UTC.

    Returns:
    int: Calculated delivery fee in cents.
    """
    if _is_eligible_for_free_delivery(cart_value):
        return 0
    delivery_fee = (
        _get_distance_fee(delivery_distance)
        + _get_small_order_surcharge(cart_value)
        + _get_item_surcharge(number_of_items)
    )
    if _is_friday_rush(time):
        delivery_fee = int(delivery_fee * FRIDAY_RUSH_MULTIPLIER)
    return min(delivery_fee, MAXIMUM_FEE)


def _is_eligible_for_free_delivery(cart_value: int) -> bool:
    return cart_value >= FREE_DELIVERY_THRESHOLD


def _get_distance_fee(distance: int) -> int:
    distance_fee = BASE_FEE

    if distance > BASE_DISTANCE:
        additional_distance = distance - BASE_DISTANCE
        distance_fee += (
            math.ceil(additional_distance / DISTANCE_UNIT) * ADDITIONAL_DISTANCE_FEE
        )

    return distance_fee


def _get_small_order_surcharge(cart_value: int) -> int:
    return max(0, SMALL_ORDER_THRESHOLD - cart_value)


def _get_item_surcharge(number_of_items: int) -> int:
    surcharge = max(0, number_of_items - ITEM_SURCHARGE_THRESHOLD) * ITEM_SURCHARGE
    if number_of_items > BULK_THRESHOLD:
        surcharge += BULK_FEE
    return surcharge


def _is_friday_rush(order_time: datetime) -> bool:
    friday_rush_start_time = time(FRIDAY_RUSH_START)
    friday_rush_end_time = time(FRIDAY_RUSH_END)
    return (
        order_time.weekday() == FRIDAY
        and friday_rush_start_time <= order_time.time() <= friday_rush_end_time
    )
