"""
indicators/rsi_calculator.py

RSI Calculator

Calculates Relative Strength Index (RSI) using
Wilder's smoothing method, matching common charting platforms.
"""

import pandas as pd


def calculate_rsi(prices, period=14):
    """
    Calculate RSI using Wilder's RSI method.

    Parameters:
        prices: pandas Series of closing prices
        period: RSI lookback period

    Returns:
        pandas Series containing RSI values
    """

    if len(prices) < period + 1:
        raise ValueError(
            "Not enough price data to calculate RSI"
        )

    delta = prices.diff()

    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)

    avg_gain = gains.ewm(
        alpha=1 / period,
        min_periods=period,
        adjust=False
    ).mean()

    avg_loss = losses.ewm(
        alpha=1 / period,
        min_periods=period,
        adjust=False
    ).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi