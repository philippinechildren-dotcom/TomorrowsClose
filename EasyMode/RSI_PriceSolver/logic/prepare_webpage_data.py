from flask import request

from EasyMode.RSI_PriceSolver.logic.calculate_signal import (
    calculate_signal,
)

from EasyMode.RSI_PriceSolver.logic.calculate_performance import (
    calculate_performance_data,
)

from catalog.strategies import get_strategy
from catalog.indicators import get_indicator

from pages.common import (
    add_common_page_data,
)


def prepare_webpage_data():

    strategy = get_strategy("rsi-pricesolver")
    indicator = get_indicator("rsi")

    ticker = request.args.get(
        "ticker",
        "QQQ",
    )

    defaults = strategy["default_parameters"][ticker]

    rsi_period = defaults["rsi_period"]

    threshold = defaults["threshold"]

    period = request.args.get(
        "period",
        "all",
    )

    signal = calculate_signal(
        ticker=ticker,
        rsi_period=rsi_period,
        threshold=threshold,
    )

    performance_data = calculate_performance_data(
        ticker=ticker,
        rsi_period=rsi_period,
        threshold=threshold,
        period=period,
    )

    result = {
        "ticker": ticker,
        "period": period,
        "rsi_period": rsi_period,
        "threshold": threshold,
        "current_price": signal["current_price"],
        "trigger_price": signal["trigger_price"],
        "status": signal["status"],
        "zone_title": signal["zone_title"],
        "execution": signal["execution"],
        "indicator": indicator,
        "performance": performance_data["performance"],
        "trade_metrics": performance_data["trade_metrics"],
        "annual_table": performance_data["annual_table"],
        "benchmark": performance_data["benchmark"],
    }

    return add_common_page_data(
        result=result,
        strategy=strategy,
        history=signal["history"],
        indicator=indicator,
    )