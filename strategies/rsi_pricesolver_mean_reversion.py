"""
RSI PriceSolver Mean Reversion Strategy

Interprets a single RSI oversold threshold.

Rules:
- Current price below trigger price:
    Oversold condition active
    Strategy status = LONG

- Current price above trigger price:
    Oversold condition not active
    Strategy status = FLAT
    Waiting for entry at trigger price

This module does not calculate RSI.
This module does not solve RSI price thresholds.
This module does not handle execution formatting.
"""


def evaluate_rsi_pricesolver_mean_reversion(
    current_price: float,
    trigger_price: float
) -> dict:
    """
    Evaluate RSI PriceSolver mean reversion status.

    Args:
        current_price: Current market close price
        trigger_price: Price where RSI reaches oversold threshold

    Returns:
        Dictionary containing strategy state and signal information
    """

    if current_price < trigger_price:
        return {
            "status": "LONG",
            "signal": "ENTRY_ACTIVE",
            "current_price": current_price,
            "trigger_price": trigger_price,
        }

    else:
        return {
            "status": "FLAT",
            "signal": "WAITING_FOR_ENTRY",
            "entry_price": trigger_price,
            "current_price": current_price,
            "trigger_price": trigger_price,
        }