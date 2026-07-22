"""
market_data/provider.py

Market Data Layer

This module is the only part of Tomorrow's Close that knows
where market data comes from.
"""

import yfinance as yf
import pandas as pd
import pandas_market_calendars as mcal

from datetime import datetime
from zoneinfo import ZoneInfo


def market_session_complete(date):
    """
    Check whether a trading session is complete.
    Uses NASDAQ calendar.
    """

    calendar = mcal.get_calendar("NASDAQ")

    schedule = calendar.schedule(
        start_date=date,
        end_date=date,
    )

    if schedule.empty:
        return False

    close_time = schedule.iloc[0]["market_close"]

    now = datetime.now(
        ZoneInfo("America/New_York")
    )

    close_time = close_time.tz_convert(
        "America/New_York"
    )

    return now >= close_time


def remove_incomplete_daily_bar(history):
    """
    Ensures only completed daily bars are returned.
    """

    latest_date = history.index[-1].date()

    if not market_session_complete(latest_date):

        history = history.iloc[:-1]

    return history


def get_market_data(ticker):
    """
    Returns the latest completed daily market data for a ticker.
    """

    stock = yf.Ticker(ticker)

    history = stock.history(
        period="5d",
        interval="1d"
    )

    if history.empty:
        raise ValueError(
            f"No market data found for ticker '{ticker}'"
        )

    history = remove_incomplete_daily_bar(
        history
    )

    latest = history.iloc[-1]

    return {
        "ticker": ticker.upper(),
        "date": str(history.index[-1].date()),
        "open": round(float(latest["Open"]), 2),
        "high": round(float(latest["High"]), 2),
        "low": round(float(latest["Low"]), 2),
        "close": round(float(latest["Close"]), 2),
        "volume": int(latest["Volume"]),
        "source": "Yahoo Finance"
    }


def get_market_history(ticker, bars=500):
    """
    Returns historical completed daily market data.

    Parameters:
        ticker: ETF or stock symbol
        bars: number of daily bars requested

    Returns:
        pandas DataFrame containing completed OHLCV data
    """

    stock = yf.Ticker(ticker)

    history = stock.history(
        period="max",
        interval="1d"
    )

    if history.empty:
        raise ValueError(
            f"No historical data found for ticker '{ticker}'"
        )

    history = remove_incomplete_daily_bar(
        history
    )

    history = history.tail(bars)

    history = history.rename(
        columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        }
    )

    history = history[
        ["open", "high", "low", "close", "volume"]
    ]

    history = history.round(2)

    return history