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

import math

def build_chart_data(
    history,
    strategy_curve,
    benchmark_curve,
):
    """
    Combine dates with normalized curves, forward-filling missing benchmark/strategy values.
    """
    chart_data = []

    last_strat = 0.0
    last_bench = 0.0

    for date, strategy_value, benchmark_value in zip(
        history.index,
        strategy_curve,
        benchmark_curve,
    ):
        # 1. Handle Strategy Value: use value, or forward-fill from previous valid price
        if math.isnan(strategy_value) or strategy_value == 0.0:
            s_val = last_strat
        else:
            s_val = round(strategy_value, 2)
            last_strat = s_val

        # 2. Handle Benchmark Value: use value, or forward-fill from previous valid price
        if math.isnan(benchmark_value) or benchmark_value == 0.0:
            b_val = last_bench
        else:
            b_val = round(benchmark_value, 2)
            last_bench = b_val

        chart_data.append(
            {
                "date": str(date.date()),
                "strategy": s_val,
                "benchmark": b_val,
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
    benchmark_ticker="QQQ",

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
    # Benchmark & Shared Inception Alignment
    # ==========================================================

    raw_benchmark_history = get_market_history(
        ticker=benchmark_ticker,
    )

    if raw_benchmark_history is None or raw_benchmark_history.empty:
        return {
            "strategy": strategy_result["name"],
            "benchmark": benchmark_ticker,
            "period": period,
            "chart_data": [],
        }

    # 1. Find the LATEST start date between Strategy and Benchmark
    common_start_date = max(history.index[0], raw_benchmark_history.index[0])
    common_end_date = min(history.index[-1], raw_benchmark_history.index[-1])

    # 2. Slice both histories to the exact same shared date range
    history = history.loc[common_start_date:common_end_date]
    benchmark_history = raw_benchmark_history.loc[common_start_date:common_end_date]

    # 3. Trim strategy equity curve to match cropped history length
    raw_strat_curve = strategy_result["equity_curve"][-len(history):]

    # 4. Compute benchmark buy-and-hold on the cropped series
    benchmark_result = build_buy_and_hold(
        closes=benchmark_history["close"],
    )

    # ==========================================================
    # Normalize Curves (Both start strictly at 0.0% on common_start_date)
    # ==========================================================

    strategy_curve = normalize_equity_curve(
        raw_strat_curve
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