from shared.order_rounding import (
    round_down_cent,
    round_up_cent,
)


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
            "execution": "Sell Limit-on-Close",
            "trigger_price": round_up_cent(trigger_price),
        }

    return {
        "status": "FLAT",
        "execution": "Buy Limit-on-Close",
        "trigger_price": round_down_cent(trigger_price),
    }