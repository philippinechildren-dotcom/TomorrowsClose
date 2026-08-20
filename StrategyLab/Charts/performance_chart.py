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

from StrategyLab.Strategies.lowhigh_ulcershield import (
    build_result as build_lowhigh_ulcershield_result,
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

    if not equity_curve:
        return []

    starting_equity = equity_curve[0]

    if starting_equity == 0:
        return [0.0 for _ in equity_curve]

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
    strategy="rsi_threshold",
    ticker="TQQQ",
    period=None,

    # RSI Threshold
    rsi_length=3,
    rsi_threshold=28,

    # LowHigh
    entry_lookback=3,
    exit_lookback=1,

    # UlcerShield
    rsi_1_period=2,
    rsi_1_threshold=28,
    rsi_2_period=3,
    rsi_2_threshold=28,
    rsi_3_period=5,
    rsi_3_threshold=28,
    rsi_4_period=8,
    rsi_4_threshold=28,
    rsi_5_period=13,
    rsi_5_threshold=32,
):
    """
    Return chart-ready performance data.
    """

    # ==========================================================
    # RSI Threshold
    # ==========================================================

    if strategy == "rsi_threshold":

        strategy_result = build_rsi_threshold_result(
            ticker=ticker,
            period=period,
            rsi_length=rsi_length,
            rsi_threshold=rsi_threshold,
        )

    # ==========================================================
    # LowHigh
    # ==========================================================

    elif strategy == "lowhigh":

        strategy_result = build_lowhigh_result(
            ticker=ticker,
            period=period,
            entry_lookback=entry_lookback,
            exit_lookback=exit_lookback,
        )

    # ==========================================================
    # Turnaround Tuesday
    # ==========================================================

    elif strategy == "turnaround_tuesday":

        strategy_result = build_turnaround_tuesday_result(
            ticker=ticker,
            period=period,
            entry_lookback=entry_lookback,
        )

    # ==========================================================
    # UlcerShield
    # ==========================================================

    elif strategy == "ulcershield":

        strategy_result = build_ulcershield_result(
            ticker=ticker,
            period=period,

            rsi_1_period=rsi_1_period,
            rsi_1_threshold=rsi_1_threshold,

            rsi_2_period=rsi_2_period,
            rsi_2_threshold=rsi_2_threshold,

            rsi_3_period=rsi_3_period,
            rsi_3_threshold=rsi_3_threshold,

            rsi_4_period=rsi_4_period,
            rsi_4_threshold=rsi_4_threshold,

            rsi_5_period=rsi_5_period,
            rsi_5_threshold=rsi_5_threshold,
        )

    # ==========================================================
    # LowHigh UlcerShield
    # ==========================================================

    elif strategy == "lowhigh_ulcershield":

        strategy_result = build_lowhigh_ulcershield_result(
            ticker=ticker,
            period=period,
            entry_lookback=entry_lookback,
            exit_lookback=exit_lookback,
        )

    else:

        raise ValueError(
            f"Unknown strategy: {strategy}"
        )

    # ==========================================================
    # Validate Strategy Result
    # ==========================================================

    if strategy_result is None:
        return {
            "strategy": "",
            "benchmark": "",
            "period": period,
            "chart_data": [],
        }

    history = strategy_result["history"]

    if history is None or history.empty:
        return {
            "strategy": strategy_result["name"],
            "benchmark": "",
            "period": period,
            "chart_data": [],
        }

    # ==========================================================
    # Benchmark
    # ==========================================================

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

    # ==========================================================
    # Normalize Curves
    # ==========================================================

    strategy_curve = normalize_equity_curve(
        strategy_result["equity_curve"]
    )

    benchmark_curve = normalize_equity_curve(
        benchmark_result["equity_curve"]
    )

    # ==========================================================
    # Return
    # ==========================================================

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