from datetime import datetime


def utc_iso_str_to_datetime(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
