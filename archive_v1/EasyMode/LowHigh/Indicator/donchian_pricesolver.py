import pandas as pd


def solve_donchian_price(
    highs: pd.Series,
    lows: pd.Series,
    closes: pd.Series,
    lookback: int,
    source: str,
) -> dict:
    """
    Calculate tomorrow's Donchian order price
    from completed daily bars.
    """

    if source == "high":

        indicator_price = highs.iloc[-lookback:].max()

        order_price = indicator_price + 0.01

    elif source == "low":

        indicator_price = lows.iloc[-lookback:].min()

        order_price = indicator_price - 0.01

    elif source == "highest_close":

        indicator_price = closes.iloc[-lookback:].max()

        order_price = indicator_price + 0.01

    elif source == "lowest_close":

        indicator_price = closes.iloc[-lookback:].min()

        order_price = indicator_price - 0.01

    else:

        raise ValueError(
            f"Unknown Donchian source: {source}"
        )

    return {

        "indicator_price": float(indicator_price),

        "exact_price": round(
            float(order_price),
            2
        ),

    }