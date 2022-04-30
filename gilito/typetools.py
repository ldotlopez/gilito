from datetime import datetime


def as_float(value):
    if isinstance(value, float):
        return value

    return float(value.replace(",", "."))


def as_datetime(value, fmt):
    if isinstance(value, datetime):
        return value
    return datetime.strptime(value, "%d/%m/%Y")


def as_currency(value):
    iso_4217 = {"€": "EUR"}
    if value not in iso_4217:
        return value

    return iso_4217[value]
