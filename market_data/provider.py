"""
market_data/provider.py

Market Data Layer

This module is the only part of Tomorrow's Close that knows
where market data comes from.
"""

import yfinance as yf


def get_market_data(ticker):
    """
    Returns the latest market data for a ticker.
    """

    stock = yf.Ticker(ticker)
    history = stock.history(period="5d")

    if history.empty:
        raise ValueError(f"No market data found for ticker '{ticker}'")

    latest = history.iloc[-1]

    return {
        "ticker": ticker.upper(),
        "close": round(float(latest["Close"]), 3),
        "date": str(history.index[-1].date()),
        "source": "Yahoo Finance"
    }
