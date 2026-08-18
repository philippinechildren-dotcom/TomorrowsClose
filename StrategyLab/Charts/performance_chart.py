"""
StrategyLab/Charts/performance_chart.py

Build chart-ready performance data.
"""

from Utilities.market_data import get_market_history
from StrategyLab.Benchmarks.buy_and_hold import (
    build_buy_and_hold,
)
from StrategyLab.Strategies.lowhigh import (
    build_result as build_lowhigh_result,
)
from StrategyLab.Strategies.turnaround_tuesday import (
    build_result as build_turnaround_tuesday_result,
)
from StrategyLab.Strategies.rsi_threshold import (
    build_result as build_rsi_threshold_result,
)
from StrategyLab.Strategies.ulcershield import (
    build_result as build_ulcershield_result,
)

# ==========================================================
# Normalize Equity Curve
# ==========================================================

def normalize_equity_curve(
    equity_curve,
):
    """
    Convert an equity curve into percent gain.

    Starting value becomes 0.00%.
    """

    starting_equity = equity_curve[0]

    return [
        (equity / starting_equity - 1) * 100
        for equity in equity_curve
    ]


# ==========================================================
# Build Chart Data
# ==========================================================

def build_chart_data(
    history,
    strategy_curve,
    benchmark_curve,
):
    """
    Combine dates with normalized curves.
    """

    chart_data = []

    for date, strategy_value, benchmark_value in zip(
        history.index,
        strategy_curve,
        benchmark_curve,
    ):

        chart_data.append(
            {
                "date": str(date.date()),
                "strategy": round(strategy_value, 2),
                "benchmark": round(benchmark_value, 2),
            }
        )

    return chart_data


# ==========================================================
# Build Performance Chart
# ==========================================================

def build_performance_chart(
    strategy="ulcershield",
    ticker="TQQQ",
    period=None,
    rsi_length=3,
    rsi_threshold=28,
    entry_lookback=1,
):
    """
    Return chart-ready performance data.
    """

    strategy_builders = {
        "rsi_threshold": build_rsi_threshold_result,
        "lowhigh": build_lowhigh_result,
        "turnaround_tuesday": build_turnaround_tuesday_result,
        "ulcershield": build_ulcershield_result,
    }

    if strategy == "rsi_threshold":

        strategy_result = build_rsi_threshold_result(
            ticker=ticker,
            period=period,
            rsi_length=rsi_length,
            rsi_threshold=rsi_threshold,
        )

    elif strategy == "turnaround_tuesday":

        strategy_result = build_turnaround_tuesday_result(
            ticker=ticker,
            period=period,
            entry_lookback=entry_lookback,
        )

    else:

        strategy_result = strategy_builders[strategy](
            ticker=ticker,
            period=period,
        )

    history = strategy_result["history"]

    benchmark_history = get_market_history(
        ticker="QQQ",
    )

    benchmark_history = benchmark_history.loc[
        history.index[0]:
        history.index[-1]
    ]

    benchmark_result = build_buy_and_hold(
        closes=benchmark_history["close"],
    )

    strategy_curve = normalize_equity_curve(
        strategy_result["equity_curve"]
    )

    benchmark_curve = normalize_equity_curve(
        benchmark_result["equity_curve"]
    )

    return {
        "strategy": strategy_result["name"],
        "benchmark": benchmark_result["name"],
        "period": period,
        "chart_data": build_chart_data(
            history,
            strategy_curve,
            benchmark_curve,
        ),
    }