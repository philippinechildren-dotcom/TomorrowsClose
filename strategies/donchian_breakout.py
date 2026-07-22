from indicators.donchian_pricesolver import (
    solve_donchian_price,
)

from shared.order_rounding import (
    round_down_cent,
    round_up_cent,
)


def calculate_donchian_breakout(
    ticker: str,
    history,
    entry_lookback: int,
    exit_lookback: int,
) -> dict:
    """
    Calculate Donchian Breakout buy and sell order zones.
    """

    entry = solve_donchian_price(
        highs=history["high"],
        lows=history["low"],
        closes=history["close"],
        lookback=entry_lookback,
        source="highest_close",
    )

    exit = solve_donchian_price(
        highs=history["high"],
        lows=history["low"],
        closes=history["close"],
        lookback=exit_lookback,
        source="lowest_close",
    )

    return {

        "ticker": ticker,

        "buy_entry": {

            "title": "Buy Entry",

            "execution": "Buy Stop",

            "trigger_price": round_up_cent(
                entry["exact_price"]
            ),

        },

        "sell_exit": {

            "title": "Sell Exit",

            "execution": "Sell Stop",

            "trigger_price": round_down_cent(
                exit["exact_price"]
            ),

        },

    }