from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pandas as pd
import pandas_market_calendars as mcal

from flask import render_template, request

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

        raise ValueError(
            f"Unknown Donchian source: {source}"
        )

    return {
        "indicator_price": float(indicator_price),
        "exact_price": float(trigger_price),
    }


def build_result(
    ticker="QQQ",
    entry_lookback=1,
    dataset="homepage",
):
    """
    Build Turnaround Tuesday PriceSolver results.

    Entry:
        Monday close only.

    The entry price is calculated from the completed trading
    session immediately preceding Monday. The preceding session
    is determined from the NASDAQ trading calendar, so holidays
    are handled automatically.

    Exit:
        Normal LowHigh-style Donchian high with a user-selected
        exit lookback.
    """

    ticker = ticker.upper()

    market_data = get_market_data(ticker)

    market_history = get_market_history(
        ticker=ticker,
        number_of_bars=200,
    )

    # ==========================================================
    # Entry
    # ==========================================================

    entry = solve_donchian_price(
        highs=market_history["high"],
        lows=market_history["low"],
        closes=market_history["close"],
        lookback=entry_lookback,
        source="low",
    )

    # ==========================================================
    # Exit
    # ==========================================================

    exit = solve_donchian_price(
        highs=market_history["high"],
        lows=market_history["low"],
        closes=market_history["close"],
        lookback=1,
        source="high",
    )

    entry_trigger = round_price_down_to_cent(
        entry["exact_price"]
    )

    exit_trigger = round_price_up_to_cent(
        exit["exact_price"]
    )

    # ==========================================================
    # Monday Entry Filter
    # ==========================================================

    current_date = datetime.now(
        ZoneInfo("America/New_York")
    ).date()

    calendar = mcal.get_calendar("NASDAQ")

    days_until_monday = (
        7 - current_date.weekday()
    ) % 7

    next_monday = (
        current_date
        + timedelta(days=days_until_monday)
    )

    monday_schedule = calendar.schedule(
        start_date=next_monday,
        end_date=next_monday,
    )

    entry_active = False

    if not monday_schedule.empty:

        monday_date = monday_schedule.index[0].date()

        previous_sessions = calendar.schedule(
            start_date=monday_date - timedelta(days=7),
            end_date=monday_date - timedelta(days=1),
        )

        if not previous_sessions.empty:

            last_session_before_monday = (
                previous_sessions.index[-1].date()
            )

            latest_market_date = (
                market_history.index[-1].date()
            )

            entry_active = (
                latest_market_date
                == last_session_before_monday
                and current_date < monday_date
            )

    # ==========================================================
    # Result
    # ==========================================================

    return {
        "dataset": dataset,
        "ticker": market_data["ticker"],
        "market_date": market_data["date"],
        "data_source": market_data["source"],
        "market_state": market_data["market_state"],
        "entry_trigger": (
            entry_trigger
            if entry_active
            else None
        ),
        "exit_trigger": exit_trigger,
        "entry_status": (
            "Active"
            if entry_active
            else "Inactive"
        ),
        "entry_lookback": entry_lookback,
        "exit_lookback": 1,
    }


def render_page():

    ticker = request.args.get(
        "etf",
        "QQQ",
    )

    entry_lookback = int(
        request.args.get(
            "entry_lookback",
            1,
        )
    )

    return render_template(
        "display_components/pricesolvers/turnaround_tuesday.html",
        result=build_result(
            ticker=ticker,
            entry_lookback=entry_lookback,
        ),
    )