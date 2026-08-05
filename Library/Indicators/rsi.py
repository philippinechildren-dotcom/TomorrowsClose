"""
Library/Indicators/rsi.py
"""

import pandas as pd


def calculate_rsi(
    closes,
    period=14,
):
    """
    Calculate Wilder's RSI exactly as TradingView.

    Parameters
    ----------
    closes : pandas.Series

        Closing prices.

    period : int

        RSI lookback.

    Returns
    -------
    pandas.Series
    """

    closes = closes.astype(float)

    delta = closes.diff()

    gains = delta.clip(lower=0.0)

    losses = -delta.clip(upper=0.0)

    rsi = pd.Series(
        index=closes.index,
        dtype=float,
    )

    if len(closes) <= period:
        return rsi

    average_gain = gains.iloc[1:period + 1].mean()

    average_loss = losses.iloc[1:period + 1].mean()

    if average_loss == 0:
        rsi.iloc[period] = 100.0
    else:
        relative_strength = average_gain / average_loss

        rsi.iloc[period] = (
            100
            - 100 / (1 + relative_strength)
        )

    for index in range(period + 1, len(closes)):

        average_gain = (
            average_gain * (period - 1)
            + gains.iloc[index]
        ) / period

        average_loss = (
            average_loss * (period - 1)
            + losses.iloc[index]
        ) / period

        if average_loss == 0:
            rsi.iloc[index] = 100.0
        else:
            relative_strength = (
                average_gain / average_loss
            )

            rsi.iloc[index] = (
                100
                - 100 / (1 + relative_strength)
            )

    return rsi