import math


def round_price_down_to_cent(price: float) -> float:
    """Round down to the nearest whole cent."""
    return math.floor(price * 100) / 100


def round_price_up_to_cent(price: float) -> float:
    """Round up to the nearest whole cent."""
    return math.ceil(price * 100) / 100