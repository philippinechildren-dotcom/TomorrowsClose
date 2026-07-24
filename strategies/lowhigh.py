from indicators.donchian_pricesolver import (
    solve_donchian_price,
)

from shared.order_rounding import (
    round_down_cent,
    round_up_cent,
)


def calculate_lowhigh(
    ticker: str,
    history,
    entry_lookback: int,
    exit_lookback: int,
) -> dict:
    """
    Calculate LowHigh buy and sell trigger zones.
    """

    entry = solve_donchian_price(
        highs=history["high"],
        lows=history["low"],
        closes=history["close"],
        lookback=entry_lookback,
        source="low",
    )

    exit = solve_donchian_price(
        highs=history["high"],
        lows=history["low"],
        closes=history["close"],
        lookback=exit_lookback,
        source="high",
    )

    return {

        "ticker": ticker,

        "entry_lookback": entry_lookback,

        "exit_lookback": exit_lookback,

        "sell_exit": {

            "execution": "Sell Limit-on-Close",

            "trigger_price": round_up_cent(
                exit["exact_price"]
            ),

        },

        "buy_entry": {

            "execution": "Buy Limit-on-Close",

            "trigger_price": round_down_cent(
                entry["exact_price"]
            ),

        },

    }