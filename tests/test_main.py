import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

MONDAY_1PM = "2024-01-15T13:00:00Z"
HTTP_OK = 200
HTTP_UNPROCESSABLE_ENTITY = 422


def test_it_accepts_valid_inputs():
    response = client.post(
        "/calculate_delivery_fee",
        json={
            "cart_value": 1000,
            "delivery_distance": 1000,
            "number_of_items": 1,
            "time": MONDAY_1PM,
        },
    )
    assert response.status_code == HTTP_OK
    assert response.json() == {"delivery_fee": 200}


@pytest.mark.parametrize(
    ("cart_value", "delivery_distance", "number_of_items"),
    [
        ("1", 1000, 1),
        (1000, "1000", 1),
        (1000, 1000, "1"),
        (-1, 1000, 1),
        (1000, -1, 1),
        (1000, 1000, -1),
    ],
    ids=[
        "String cart_value",
        "String delivery_distance",
        "String number_of_items",
        "Negative cart value",
        "Negative delivery distance",
        "Negative number of items",
    ],
)
def test_it_rejects_invalid_integer_input(
    cart_value: int,
    delivery_distance: int,
    number_of_items: int,
):
    response = client.post(
        "/calculate_delivery_fee",
        json={
            "cart_value": cart_value,
            "delivery_distance": delivery_distance,
            "number_of_items": number_of_items,
            "time": MONDAY_1PM,
        },
    )
    assert response.status_code == HTTP_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    ("time"),
    [
        ("NOT_TIME_AT_ALL"),
        ("2024-01-15 13:00:00Z"),
        ("2024-01-15T13:00:00"),
        ("2024-13-15T13:00:00Z"),
        ("2024-00-15T13:00:00Z"),
        ("2024-01-00T13:00:00Z"),
        ("2024-01-15T25:00:00Z"),
        ("2024-01-15T13:60:00Z"),
        ("2024-01-15T13:00:60Z"),
    ],
    ids=[
        "Invalid string",
        "Missing T",
        "Missing Z",
        "Invalid year",
        "Invalid month",
        "Invalid day",
        "Invalid hour",
        "Invalid minute",
        "Invalid second",
    ],
)
def test_it_rejects_invalid_time_input(time: str):
    response = client.post(
        "/calculate_delivery_fee",
        json={
            "cart_value": 1000,
            "delivery_distance": 1000,
            "number_of_items": 1,
            "time": time,
        },
    )
    assert response.status_code == HTTP_UNPROCESSABLE_ENTITY


def test_it_calculates_delivery_fee():
    response = client.post(
        "/calculate_delivery_fee",
        json={
            "cart_value": 790,
            "delivery_distance": 2235,
            "number_of_items": 4,
            "time": MONDAY_1PM,
        },
    )
    assert response.status_code == HTTP_OK
    assert response.json() == {"delivery_fee": 710}
