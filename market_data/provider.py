"""
market_data/provider.py

Market Data Layer

This module is the only part of Tomorrow's Close that knows
where market data comes from.

Version 0.1 returns dummy data for testing.
"""


def get_market_data(ticker):
    """
    Returns market data for a ticker.

    Parameters
    ----------
    ticker : str

    Returns
    -------
    dict
    """

    return {
        "ticker": ticker.upper(),
        "close": 527.183,
        "date": "2026-07-20",
        "source": "Dummy Data"
    }
