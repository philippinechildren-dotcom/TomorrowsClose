"""
Utilities/market_data.py

Market data for Tomorrow's Close.

This module is the only part of the application that knows
where market data comes from.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import pandas_market_calendars as mcal
import yfinance as yf
SETTLEMENT_DELAY_MINUTES = 30

def _market_session_complete(date):
    """
    Returns True when the NASDAQ trading session has completed.
    """

    calendar = mcal.get_calendar("NASDAQ")

    schedule = calendar.schedule(
        start_date=date,
        end_date=date,
    )

    if schedule.empty:
        return False

    close_time = schedule.iloc[0]["market_close"]

    current_time = datetime.now(
        ZoneInfo("America/New_York")
    )

    close_time = close_time.tz_convert(
        "America/New_York"
    )

    return current_time >= close_time

from datetime import timedelta


def _market_state():
    """
    Returns 'settlement' while waiting for the official
    daily close to become available.
    """

    current_time = datetime.now(
        ZoneInfo("America/New_York")
    )

    calendar = mcal.get_calendar("NASDAQ")

    schedule = calendar.schedule(
        start_date=current_time.date(),
        end_date=current_time.date(),
    )

    if schedule.empty:
        return "current"

    close_time = schedule.iloc[0]["market_close"].tz_convert(
        "America/New_York"
    )

    settlement_complete = close_time + timedelta(
        minutes=SETTLEMENT_DELAY_MINUTES
    )

    if close_time <= current_time < settlement_complete:
        return "settlement"

    return "current"

def _remove_incomplete_daily_bar(history):
    """
    Removes today's bar if the trading session has not finished.
    """

    latest_date = history.index[-1].date()

    if not _market_session_complete(latest_date):
        history = history.iloc[:-1]

    return history


def get_market_data(ticker):
    """
    Returns the latest completed daily market data.
    """

    stock = yf.Ticker(ticker)

    history = stock.history(
        period="5d",
        interval="1d",
        auto_adjust=False,
        repair=False,
        prepost=False,
    )

    if history.empty:
        raise ValueError(
            f"No market data found for ticker '{ticker}'."
        )

    history = _remove_incomplete_daily_bar(history)
    latest_bar = history.iloc[-1]
    current_time = datetime.now(
        ZoneInfo("America/New_York")
    )

    last_updated = current_time.strftime(
        "%B %d, %Y %I:%M %p ET"
    )

    return {
        "ticker": ticker.upper(),
        "date": str(history.index[-1].date()),
        "open": round(float(latest_bar["Open"]), 2),
        "high": round(float(latest_bar["High"]), 2),
        "low": round(float(latest_bar["Low"]), 2),
        "close": round(float(latest_bar["Close"]), 2),
        "volume": int(latest_bar["Volume"]),
        "source": "Yahoo Finance",
        "last_updated": last_updated,
        "market_state": _market_state(),
    }

def get_market_history(ticker, number_of_bars=None):
    """
    Returns completed historical daily market data.
    """

    stock = yf.Ticker(ticker)

    history = stock.history(
        period="max",
        interval="1d",
        auto_adjust=False,
        repair=False,
        prepost=False,
    )

    if history.empty:
        raise ValueError(
            f"No historical data found for ticker '{ticker}'."
        )

    history = _remove_incomplete_daily_bar(history)

    if number_of_bars is not None:
        history = history.tail(number_of_bars)

    history = history.rename(
        columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        }
    )

    history = history[
        ["open", "high", "low", "close", "volume"]
    ]

    return history.round(2)

def filter_history(
    history,
    period=None,
):
    """
    Filter market history.

    period

        None
        "1_month"
        "3_months"
        "6_months"
        "ytd"
        "1_year"
        "2_years"
        "3_years"
        "5_years"
        "10_years"
        "maximum"
    """

    if period is None or period == "maximum":
        return history

    if period == "ytd":

        current_year = datetime.now(
            ZoneInfo("America/New_York")
        ).year

        return history[
            history.index.year == current_year
        ]

    if isinstance(period, str):

        period_lookup = {
            "1_month": 1 / 12,
            "3_months": 0.25,
            "6_months": 0.5,
            "1_year": 1,
            "2_years": 2,
            "3_years": 3,
            "5_years": 5,
            "10_years": 10,
        }

        period = period_lookup[period]

    else:

        period = float(period)

    performance_days = int(
        252 * period
    )

    if len(history) <= performance_days:
        return history

    return history.iloc[
        -performance_days:
    ]