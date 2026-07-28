from flask import request

from catalog.strategies import get_strategy

from EasyMode.RSI_PriceSolver.performance.build_strategy import (
    build_rsi_pricesolver,
)

from Other_Strategies.Trend_Following.Buy_and_Hold.performance.build_strategy import (
    build_buy_and_hold,
)

from analytics.performance.metrics import (
    calculate_performance,
)


def build_performance_summary_vertical(
    strategy: str,
    period: str = "all",
):

    strategy_metadata = get_strategy(strategy)

    ticker = request.args.get(
        "ticker",
        "QQQ",
    )

    defaults = strategy_metadata["default_parameters"][ticker]

    rsi_period = defaults["rsi_period"]

    threshold = defaults["threshold"]

    strategy_result = build_rsi_pricesolver(
        ticker=ticker,
        rsi_length=rsi_period,
        threshold=threshold,
        period=period,
    )

    strategy_result["performance"] = calculate_performance(
        strategy_result["equity_curve"],
        strategy_result.get("closed_equity"),
    )

    benchmark_result = build_buy_and_hold(
        ticker="QQQ",
        period=period,
    )

    benchmark_result["performance"] = calculate_performance(
        benchmark_result["equity_curve"],
    )

    return {
        "period": period,
        "ticker": ticker,
        "rsi_period": rsi_period,
        "threshold": threshold,
        "performance": strategy_result["performance"],
        "trade_metrics": strategy_result["trade_metrics"],
        "benchmark": benchmark_result,
    }