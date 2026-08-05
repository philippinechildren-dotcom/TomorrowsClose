"""
Library/Indicators/donchian.py
"""

def calculate_donchian(
    highs,
    lows,
    upper_lookback,
    lower_lookback,
):
    """
    Calculate Donchian Channel.

    Parameters
    ----------
    highs : Series
    lows : Series
    upper_lookback : int
    lower_lookback : int

    Returns
    -------
    tuple
        (upper_band, lower_band)

    Current bar is excluded from both calculations.
    """

    upper_band = highs.shift(1).rolling(upper_lookback).max()

    lower_band = lows.shift(1).rolling(lower_lookback).min()

    return upper_band, lower_band