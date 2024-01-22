from fastapi.testclient import TestClient
import pytest
from app.main import app

client = TestClient(app)

MONDAY_1PM = "2024-01-15T13:00:00Z"


def test_accepts_valid_inputs():
    response = client.post(
        "/calculate_delivery_fee",
        json={
            "cart_value": 1000,
            "delivery_distance": 1000,
            "number_of_items": 1,
            "time": MONDAY_1PM,
        },
    )
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 200}


@pytest.mark.parametrize(
    "_description, cart_value, delivery_distance, number_of_items",
    [
        ("String cart_value", "1", 1000, 1),
        ("String delivery_distance", 1000, "1000", 1),
        ("String number_of_items", 1000, 1000, "1"),
        ("Negative cart value", -1, 1000, 1),
        ("Negative delivery distance", 1000, -1, 1),
        ("Negative number of items", 1000, 1000, -1),
    ],
    ids=lambda _description: _description,
)
def test_rejects_invalid_integer_input(
    _description: str,
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
    assert response.status_code == 422


@pytest.mark.parametrize(
    "_description, time",
    [
        ("Invalid string", "NOT_TIME_AT_ALL"),
        ("Missing T", "2024-01-15 13:00:00Z"),
        ("Missing Z", "2024-01-15T13:00:00"),
        ("Invalid year", "2024-13-15T13:00:00Z"),
        ("Invalid month", "2024-00-15T13:00:00Z"),
        ("Invalid day", "2024-01-00T13:00:00Z"),
        ("Invalid hour", "2024-01-15T25:00:00Z"),
        ("Invalid minute", "2024-01-15T13:60:00Z"),
        ("Invalid second", "2024-01-15T13:00:60Z"),
    ],
)
def test_rejects_invalid_time_input(_description: str, time: str):
    response = client.post(
        "/calculate_delivery_fee",
        json={
            "cart_value": 1000,
            "delivery_distance": 1000,
            "number_of_items": 1,
            "time": time,
        },
    )
    assert response.status_code == 422


def test_calculates_delivery_fee():
    response = client.post(
        "/calculate_delivery_fee",
        json={
            "cart_value": 790,
            "delivery_distance": 2235,
            "number_of_items": 4,
            "time": MONDAY_1PM,
        },
    )
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 710}
