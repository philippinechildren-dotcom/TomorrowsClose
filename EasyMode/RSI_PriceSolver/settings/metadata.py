from catalog.strategies import get_strategy
from catalog.indicators import get_indicator


def get_strategy_metadata():

    return get_strategy(
        "rsi-pricesolver",
    )


def get_indicator_metadata():

    return get_indicator(
        "rsi",
    )