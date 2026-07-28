from EasyMode.RSI_PriceSolver.performance.strategy_performance import (
    calculate_strategy_performance,
)


def calculate_performance_data(
    ticker,
    rsi_period,
    threshold,
    period,
):
    return calculate_strategy_performance(
        ticker=ticker,
        rsi_period=rsi_period,
        threshold=threshold,
        period=period,
    )