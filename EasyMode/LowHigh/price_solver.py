from flask import render_template, request

import pandas as pd

from Utilities.market_data import (
    get_market_data,
    get_market_history,
)

from Utilities.order_rounding import (
    round_price_down_to_cent,
    round_price_up_to_cent,
)


def solve_donchian_price(
    highs: pd.Series,
    lows: pd.Series,
    closes: pd.Series,
    lookback: int,
    source: str,
) -> dict:
    """
    Calculate the Donchian trigger price from completed daily bars.
    """

    if source == "high":
        indicator_price = highs.iloc[-lookback:].max()
        trigger_price = indicator_price + 0.01

    elif source == "low":
        indicator_price = lows.iloc[-lookback:].min()
        trigger_price = indicator_price - 0.01

    elif source == "highest_close":
        indicator_price = closes.iloc[-lookback:].max()
        trigger_price = indicator_price + 0.01

    elif source == "lowest_close":
        indicator_price = closes.iloc[-lookback:].min()
        trigger_price = indicator_price - 0.01

    else:
        raise ValueError(f"Unknown Donchian source: {source}")

    return {
        "indicator_price": float(indicator_price),
        "exact_price": round(float(trigger_price), 2),
    }


def evaluate_lowhigh(
    current_price: float,
    entry_trigger: float,
    exit_trigger: float,
) -> dict:
    """
    Determine whether the strategy is currently LONG or FLAT.
    """

    if current_price < exit_trigger:
        return {
            "status": "LONG",
            "execution": "Sell Limit-on-Close",
            "trigger_price": round_price_up_to_cent(exit_trigger),
        }

    return {
        "status": "FLAT",
        "execution": "Buy Limit-on-Close",
        "trigger_price": round_price_down_to_cent(entry_trigger),
    }


def build_result(
    ticker="QLD",
    entry_lookback=3,
    exit_lookback=1,
    dataset="homepage",
):

    ticker = ticker.upper()

    market_data = get_market_data(ticker)

    market_history = get_market_history(
        ticker=ticker,
        number_of_bars=200,
    )

    entry = solve_donchian_price(
        highs=market_history["high"],
        lows=market_history["low"],
        closes=market_history["close"],
        lookback=entry_lookback,
        source="low",
    )

    exit = solve_donchian_price(
        highs=market_history["high"],
        lows=market_history["low"],
        closes=market_history["close"],
        lookback=exit_lookback,
        source="high",
    )

    signal = evaluate_lowhigh(
        current_price=market_data["close"],
        entry_trigger=entry["exact_price"],
        exit_trigger=exit["exact_price"],
    )
    
    return {
        "dataset": dataset,
        "ticker": market_data["ticker"],
        "market_date": market_data["date"],
        "data_source": market_data["source"],
        "market_state": market_data["market_state"],
        "status": signal["status"],
        "trigger_price": signal["trigger_price"],
        "execution": signal["execution"],
        "entry_lookback": entry_lookback,
        "exit_lookback": exit_lookback,
    }


def render_page():

    ticker = request.args.get("ticker", "QLD")

    entry_lookback = int(
        request.args.get(
            "entry_lookback",
            3,
        )
    )

    exit_lookback = int(
        request.args.get(
            "exit_lookback",
            1,
        )
    )

    return render_template(
        "lowhigh.html",
        result=build_result(
            ticker=ticker,
            entry_lookback=entry_lookback,
            exit_lookback=exit_lookback,
        ),
    )