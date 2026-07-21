import math


def round_down_cent(price: float) -> float:
    return math.floor(price * 100) / 100


def round_up_cent(price: float) -> float:
    return math.ceil(price * 100) / 100