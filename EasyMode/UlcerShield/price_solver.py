from flask import render_template, request

from EasyMode.RSI_PriceSolver.rsi_solver import solve_rsi_price

from Utilities.market_data import (
    get_market_data,
    get_market_history,
)

from Utilities.order_rounding import (
    round_price_down_to_cent,
    round_price_up_to_cent,
)


def evaluate_ulcershield_component(
    current_price: float,
    trigger_price: float,
) -> dict:
    """
    Evaluate one UlcerShield component.
    """

    if current_price < trigger_price:

        return {
            "status": "LONG",
            "execution": "Sell Limit-on-Close",
            "trigger_price": round_price_up_to_cent(trigger_price),
        }

    return {
        "status": "FLAT",
        "execution": "Buy Limit-on-Close",
        "trigger_price": round_price_down_to_cent(trigger_price),
    }


def build_result(
    ticker="TQQQ",
    systems=None,
    dataset="homepage",
):

    ticker = ticker.upper()

    if systems is None:

        systems = [
            {"name": "RSI1", "period": 2, "threshold": 28},
            {"name": "RSI2", "period": 3, "threshold": 28},
            {"name": "RSI3", "period": 5, "threshold": 28},
            {"name": "RSI4", "period": 8, "threshold": 28},
            {"name": "RSI5", "period": 13, "threshold": 32},
        ]

    market_data = get_market_data(ticker)

    market_history = get_market_history(
        ticker=ticker,
        number_of_bars=500,
    )

    closing_prices = market_history["close"].tolist()

    components = []

    campaign_status = "FLAT"

    for system in systems:

        solver_result = solve_rsi_price(
            closes=closing_prices,
            period=system["period"],
            target=system["threshold"],
        )

        component = evaluate_ulcershield_component(
            current_price=market_data["close"],
            trigger_price=solver_result["exact_price"],
        )

        if component["status"] == "LONG":
            campaign_status = "ACTIVE"

        components.append(
            {
                "name": system["name"],
                "period": system["period"],
                "threshold": system["threshold"],
                "status": component["status"],
                "execution": component["execution"],
                "trigger_price": component["trigger_price"],
            }
        )

    return {
        "dataset": dataset,
        "ticker": market_data["ticker"],
        "market_date": market_data["date"],
        "data_source": market_data["source"],
        "market_state": market_data["market_state"],
        "campaign_status": campaign_status,
        "systems": systems,
        "components": components,
    }

def render_page():

    ticker = request.args.get(
        "ticker",
        "TQQQ",
    ).upper()

    systems = [
        {
            "name": "RSI1",
            "period": int(request.args.get("period1", 2)),
            "threshold": int(request.args.get("threshold1", 28)),
        },
        {
            "name": "RSI2",
            "period": int(request.args.get("period2", 3)),
            "threshold": int(request.args.get("threshold2", 28)),
        },
        {
            "name": "RSI3",
            "period": int(request.args.get("period3", 5)),
            "threshold": int(request.args.get("threshold3", 28)),
        },
        {
            "name": "RSI4",
            "period": int(request.args.get("period4", 8)),
            "threshold": int(request.args.get("threshold4", 28)),
        },
        {
            "name": "RSI5",
            "period": int(request.args.get("period5", 13)),
            "threshold": int(request.args.get("threshold5", 32)),
        },
    ]

    return render_template(
        "ulcershield.html",
        result=build_result(
            ticker=ticker,
            systems=systems,
        ),
    )