"""
StrategyLab/Benchmarks/buy_and_hold.py
"""

from Utilities.market_data import (
    get_market_history,
    filter_history,
)

from StrategyLab.Metrics.metrics import build_metrics


def build_buy_and_hold(
    closes,
    starting_equity=100000.0,
):
    """
    Build Buy & Hold benchmark statistics.
    """

    if len(closes) == 0:
        return None

    # ==========================================================
    # Buy & Hold Position
    # ==========================================================

    entry_price = float(closes.iloc[0])
    ending_price = float(closes.iloc[-1])

    shares = starting_equity / entry_price

    equity_curve = [
        shares * float(close)
        for close in closes
    ]

    ending_equity = equity_curve[-1]

    years = (
        (closes.index[-1] - closes.index[0]).days
        / 365.25
    )

    # ==========================================================
    # Metrics
    # ==========================================================

    metrics = build_metrics(
        equity_curve=equity_curve,
        trades=[],
        starting_equity=starting_equity,
        ending_equity=ending_equity,
        years=years,
        exposure=1.0,
    )

    # ==========================================================
    # Buy & Hold does not have trades
    # ==========================================================

    metrics["max_closed_trade_drawdown"] = None
    metrics["win_rate"] = None
    metrics["expectancy_percent"] = None

    # ==========================================================
    # Benchmark
    # ==========================================================

    return {
        "name": "Buy & Hold",
        "type": "benchmark",
        "entry_price": entry_price,
        "ending_price": ending_price,
        "shares": shares,
        "starting_equity": starting_equity,
        "ending_equity": ending_equity,
        "equity_curve": equity_curve,
        "years": years,
        "exposure": 1.0,
        "metrics": metrics,
    }


def build_result(
    ticker="QQQ",
    period=None,
    starting_equity=100000.0,
):
    """
    Build a complete Buy & Hold benchmark using current market data.
    """

    history = get_market_history(
        ticker=ticker,
    )

    history = filter_history(
        history,
        period,
    )

    return build_buy_and_hold(
        closes=history["close"],
        starting_equity=starting_equity,
    )