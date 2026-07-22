from flask import request

from market_data.provider import get_market_history

from indicators.rsi_pricesolver import (
    solve_rsi_price,
)

from strategies.rsi_pricesolver_mean_reversion import (
    evaluate_rsi_pricesolver_mean_reversion,
)

from catalog.strategies import get_strategy
from catalog.indicators import get_indicator

from pages.common import (
    add_common_page_data,
)


def build_result():

    strategy = get_strategy("rsi-pricesolver")

    indicator = get_indicator("rsi")

    defaults = strategy["default_parameters"]

    ticker = request.args.get(
        "ticker",
        defaults["ticker"]
    )

    rsi_period = int(
        request.args.get(
            "rsi_period",
            defaults["rsi_period"]
        )
    )

    threshold = int(
        request.args.get(
            "threshold",
            defaults["threshold"]
        )
    )

    history = get_market_history(
        ticker,
        bars=500
    )

    solver_result = solve_rsi_price(
        closes=history["close"],
        period=rsi_period,
        target=threshold
    )

    current_price = history["close"].iloc[-1]

    strategy_result = evaluate_rsi_pricesolver_mean_reversion(
        current_price=current_price,
        trigger_price=solver_result["exact_price"]
    )

    result = {

        "ticker": ticker,

        "rsi_period": rsi_period,

        "threshold": threshold,

        "current_price": round(
            float(current_price),
            2
        ),

        "trigger_price": strategy_result["trigger_price"],

        "status": strategy_result["status"],

        "execution": strategy_result["execution"],

        "indicator": indicator,

    }

    return add_common_page_data(
        result=result,
        strategy=strategy,
        history=history,
        indicator=indicator,
    )