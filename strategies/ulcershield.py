from indicators.rsi_pricesolver import solve_rsi_price

from shared.order_rounding import (
    round_down_cent,
    round_up_cent,
)


def evaluate_ulcershield_component(
    current_price: float,
    trigger_price: float
) -> dict:
    """
    Evaluate one UlcerShield RSI component.
    """

    if current_price < trigger_price:

        return {

            "status": "LONG",

            "execution": "Sell Limit-on-Close",

            "trigger_price": round_up_cent(
                trigger_price
            ),

        }

    return {

        "status": "FLAT",

        "execution": "Buy Limit-on-Close",

        "trigger_price": round_down_cent(
            trigger_price
        ),

    }

def calculate_ulcershield(
    ticker: str,
    history,
    rsi_systems: list
) -> dict:
    """
    Calculate all UlcerShield RSI components.
    Uses metadata as the source of RSI parameters.
    """

    current_price = history["close"].iloc[-1]

    components = []

    for system in rsi_systems:

        solver_result = solve_rsi_price(
            closes=history["close"],
            period=system["period"],
            target=system["threshold"],
        )

        result = evaluate_ulcershield_component(
            current_price=current_price,
            trigger_price=solver_result["exact_price"],
        )

        components.append(
            {
                "name": system["name"],
                **result,
            }
        )

    campaign_status = "FLAT"

    for component in components:

        if component["status"] == "LONG":
            campaign_status = "ACTIVE"
            break

    return {

        "ticker": ticker,

        "current_price": round(
            float(current_price),
            2
        ),

        "campaign_status": campaign_status,

        "components": components,

    }