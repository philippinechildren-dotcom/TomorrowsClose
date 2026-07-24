from flask import request

from market_data.provider import get_market_history

from strategies.ulcershield import (
    calculate_ulcershield,
)

from analytics.strategies.build_ulcershield import (
    build_ulcershield,
)

from analytics.performance.metrics import (
    calculate_performance,
)

from catalog.strategies import get_strategy

from pages.common import (
    add_common_page_data,
)


def build_result():

    strategy = get_strategy("ulcershield")

    defaults = strategy["default_parameters"]

    ticker = request.args.get(
        "ticker",
        defaults["ticker"]
    )

    history = get_market_history(
        ticker,
        bars=500
    )

    result = calculate_ulcershield(
        ticker=ticker,
        history=history,
        rsi_systems=strategy["rsi_systems"]
    )

    performance_result = build_ulcershield(
        ticker=ticker,
    )

    result["performance"] = calculate_performance(
        performance_result["equity_curve"]
    )

    return add_common_page_data(
        result=result,
        strategy=strategy,
        history=history,
    )