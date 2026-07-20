"""
market_data/provider.py

Market Data Layer

This module is the only part of Tomorrow's Close that knows
where market data comes from.
"""

import yfinance as yf
import pandas as pd


def get_market_data(ticker):
    """
    Returns the latest daily market data for a ticker.
    """

    stock = yf.Ticker(ticker)
    history = stock.history(period="5d")

    if history.empty:
        raise ValueError(f"No market data found for ticker '{ticker}'")

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
    Returns historical daily market data for a ticker.

    Parameters:
        ticker: ETF or stock symbol
        bars: number of daily bars requested

    Returns:
        pandas DataFrame containing OHLCV data
    """

    stock = yf.Ticker(ticker)

    history = stock.history(
        period="max",
        interval="1d"
    )

    if history.empty:
        raise ValueError(f"No historical data found for ticker '{ticker}'")

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