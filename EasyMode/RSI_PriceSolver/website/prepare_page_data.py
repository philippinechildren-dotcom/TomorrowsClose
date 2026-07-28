from flask import request

from EasyMode.RSI_PriceSolver.logic.calculate_signal import calculate_signal
from EasyMode.RSI_PriceSolver.performance.calculate_performance import calculate_performance_data
from EasyMode.RSI_PriceSolver.settings.defaults import get_defaults
from EasyMode.RSI_PriceSolver.settings.metadata import (
    get_strategy_metadata,
    get_indicator_metadata,
)
from EasyMode.RSI_PriceSolver.website.page_data import add_page_data

def prepare_page_data():
    strategy = get_strategy_metadata()
    indicator = get_indicator_metadata()

    ticker = request.args.get("ticker", "QQQ")
    defaults = get_defaults(ticker=ticker)

    rsi_period = int(request.args.get(
        "rsi_period",
        defaults["rsi_period"],
    ))

    threshold = float(request.args.get(
        "threshold",
        defaults["threshold"],
    ))

    period = request.args.get("period", "all")

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

    return add_page_data(
        result=result,
        strategy=strategy,
        history=signal["history"],
        indicator=indicator,
    )