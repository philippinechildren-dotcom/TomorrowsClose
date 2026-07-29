"""
indicators/rsi_pricesolver.py

RSI PriceSolver

Calculates the future closing price required to reach
a target RSI value using Wilder's RSI calculation.

The solver returns the mathematical price target.
Execution rounding belongs in a separate layer.
"""


def solve_rsi_price(closes, period, target):
    closes = list(closes)
    """
    Solve for the closing price required to reach a target RSI.

    Parameters:
        closes: list or pandas Series of closing prices
        period: RSI period
        target: target RSI value

    Returns:
        dictionary containing projected price information
    """

    gains = []
    losses = []

    # --------------------------------
    # Build gain/loss arrays
    # --------------------------------
    for i in range(1, len(closes)):

        change = closes[i] - closes[i - 1]

        gains.append(max(change, 0))
        losses.append(max(-change, 0))

    # --------------------------------
    # Wilder RSI Initialization
    # SMA seed like TradingView
    # --------------------------------
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    # --------------------------------
    # Recursive Wilder smoothing
    # --------------------------------
    for i in range(period, len(gains)):

        avg_gain = ((avg_gain * (period - 1)) + gains[i]) / period
        avg_loss = ((avg_loss * (period - 1)) + losses[i]) / period

    # --------------------------------
    # Current RSI
    # --------------------------------
    if avg_gain + avg_loss == 0:
        current_rsi = 50
    else:
        current_rsi = 100 * avg_gain / (avg_gain + avg_loss)

    # --------------------------------
    # Inverse RSI price projection
    # --------------------------------
    target_rs = target / (100 - target)

    if target > current_rsi:

        delta = (
            target_rs * avg_loss * (period - 1)
            - avg_gain * (period - 1)
        )

        direction = "above"

    else:

        delta = (
            avg_loss * (period - 1)
            - ((100 - target) / target)
            * avg_gain * (period - 1)
        )

        direction = "below"

    projected_price = closes[-1] + delta

    return {
        "current_rsi": current_rsi,
        "target_rsi": target,
        "exact_price": projected_price,
    }