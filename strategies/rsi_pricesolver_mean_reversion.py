def evaluate_rsi_pricesolver_mean_reversion(
    current_price: float,
    trigger_price: float
) -> dict:
    """
    Evaluate RSI PriceSolver mean reversion status.
    """

    if current_price < trigger_price:

        return {
            "status": "LONG",
            "signal": "SELL EXIT",
            "comparison": "Close Above",
            "execution": "Limit-on-Close",
            "rounding": "UP",
            "trigger_price": trigger_price,
        }

    return {
        "status": "FLAT",
        "signal": "BUY ENTRY",
        "comparison": "Close Below",
        "execution": "Limit-on-Close",
        "rounding": "DOWN",
        "trigger_price": trigger_price,
    }