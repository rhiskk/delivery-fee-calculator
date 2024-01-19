from typing import TypedDict


class Order(TypedDict):
    cart_value: int
    delivery_distance: int
    number_of_items: int
    time: str


def calculate_delivery_fee(order: Order) -> int:
    print(order)
    return 310
