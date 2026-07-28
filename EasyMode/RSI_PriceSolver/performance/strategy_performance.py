from EasyMode.RSI_PriceSolver.performance.performance_pipeline import (
    calculate_strategy_results,
)
from Other_Strategies.Trend_Following.Buy_and_Hold.performance.build_strategy import (
    build_buy_and_hold,
)
from analytics.performance.metrics import calculate_performance

def calculate_strategy_performance(
    ticker,
    rsi_period,
    threshold,
    period,
):
    performance_result = calculate_strategy_results(
        ticker=ticker,
        rsi_length=rsi_period,
        threshold=threshold,
        period=period,
    )

    performance = calculate_performance(
        performance_result["equity_curve"],
        performance_result.get("closed_equity"),
    )

    benchmark_result = build_buy_and_hold(
        ticker="QQQ",
        period=period,
    )

    benchmark_result["performance"] = calculate_performance(
        benchmark_result["equity_curve"],
    )

    return {
        "performance": performance,
        "trade_metrics": performance_result["trade_metrics"],
        "annual_table": performance_result["annual_table"],
        "benchmark": benchmark_result,
    }