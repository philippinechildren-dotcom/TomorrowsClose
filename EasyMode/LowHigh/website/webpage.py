from flask import request

from market_data.provider import get_market_history

from strategies.lowhigh import (
    calculate_lowhigh,
)

from EasyMode.LowHigh.performance.build_strategy import (
    build_lowhigh,
)

from analytics.performance.metrics import (
    calculate_performance,
)

from catalog.strategies import get_strategy

from pages.common import (
    add_common_page_data,
)


def build_result():

    strategy = get_strategy("lowhigh")

    defaults = strategy["default_parameters"]

    ticker = request.args.get(
        "ticker",
        defaults["ticker"]
    )

    entry_lookback = int(
        request.args.get(
            "entry_lookback",
            defaults["entry_lookback"]
        )
    )

    exit_lookback = int(
        request.args.get(
            "exit_lookback",
            defaults["exit_lookback"]
        )
    )

    period = request.args.get(
        "period",
        defaults.get("period", "1y")
    )

    history = get_market_history(
        ticker,
        bars=500
    )

    result = calculate_lowhigh(
        ticker=ticker,
        history=history,
        entry_lookback=entry_lookback,
        exit_lookback=exit_lookback,
    )

    performance_result = build_lowhigh(
        ticker=ticker,
        entry_lookback=entry_lookback,
        exit_lookback=exit_lookback,
        period=period,
    )

    result["performance"] = calculate_performance(
        performance_result["equity_curve"],
        performance_result.get("closed_equity"),
    )

    result["trade_metrics"] = performance_result["trade_metrics"]

    result["period"] = period

    return add_common_page_data(
        result=result,
        strategy=strategy,
        history=history,
    )