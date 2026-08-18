"""
StrategyLab/Strategies/turnaround_tuesday.py
"""

from Utilities.market_data import (
    get_market_history,
    filter_history,
)

from Library.Trading.trade_engine import build_trades
from StrategyLab.Metrics.metrics import build_metrics


def build_turnaround_tuesday(
    history,
    entry_lookback=1,
    starting_equity=100000.0,
):
    """
    Build Turnaround Tuesday strategy statistics.

    Entry:
        Monday close < lowest low of the preceding
        entry_lookback completed trading sessions.

    Exit:
        Close > previous trading day's high.

    All orders execute at the closing price.
    """

    if history.empty:
        return None

    signals = []
    in_position = False

    for index in range(len(history)):

        date = history.index[index]
        close = float(history.iloc[index]["close"])

        # ------------------------------------------------------
        # Entry
        # ------------------------------------------------------

        if not in_position and date.weekday() == 0:

            if index < entry_lookback:
                continue

            previous_history = history.iloc[
                index - entry_lookback:index
            ]

            lowest_low = float(
                previous_history["low"].min()
            )

            if close < lowest_low:

                signals.append({
                    "date": date,
                    "signal": "BUY",
                    "price": close,
                })

                in_position = True

        # ------------------------------------------------------
        # Exit
        # ------------------------------------------------------

        elif in_position and index >= 1:

            previous_high = float(
                history.iloc[index - 1]["high"]
            )

            if close > previous_high:

                signals.append({
                    "date": date,
                    "signal": "SELL",
                    "price": close,
                })

                in_position = False

    # ==========================================================
    # Trades
    # ==========================================================

    trade_results = build_trades(
        signals=signals,
        starting_equity=starting_equity,
    )

    trades = trade_results["trades"]

    # ==========================================================
    # Daily Equity Curve
    # ==========================================================

    equity_curve = []
    equity = starting_equity
    trade_number = 0
    shares = 0.0
    in_position = False

    for date, row in history.iterrows():

        close = float(row["close"])

        if (
            trade_number < len(trades)
            and date == trades[trade_number].entry_date
        ):

            shares = (
                equity
                / trades[trade_number].entry_price
            )

            in_position = True

        equity_curve.append(
            shares * close
            if in_position
            else equity
        )

        if (
            trade_number < len(trades)
            and date == trades[trade_number].exit_date
        ):

            equity = (
                shares
                * trades[trade_number].exit_price
            )

            in_position = False
            trade_number += 1

    ending_equity = equity_curve[-1]

    years = (
        (history.index[-1] - history.index[0]).days
        / 365.25
    )

    # ==========================================================
    # Exposure
    # ==========================================================

    days_in_market = sum(
        trade.days_held
        for trade in trades
    )

    total_days = len(history)

    exposure = (
        days_in_market / total_days
        if total_days > 0
        else 0.0
    )

    # ==========================================================
    # Metrics
    # ==========================================================

    metrics = build_metrics(
        equity_curve=equity_curve,
        trades=trades,
        starting_equity=starting_equity,
        ending_equity=ending_equity,
        years=years,
        exposure=exposure,
    )

    # ==========================================================
    # Strategy
    # ==========================================================

    return {
        "name": "Turnaround Tuesday",
        "type": "strategy",
        "starting_equity": starting_equity,
        "ending_equity": ending_equity,
        "history": history,
        "equity_curve": equity_curve,
        "trades": trades,
        "years": years,
        "metrics": metrics,
    }


def build_result(
    ticker="QQQ",
    period=None,
    entry_lookback=1,
    starting_equity=100000.0,
):
    """
    Build a complete Turnaround Tuesday strategy
    using current market data.
    """

    history = get_market_history(
        ticker=ticker,
    )

    history = filter_history(
        history,
        period,
    )

    return build_turnaround_tuesday(
        history=history,
        entry_lookback=entry_lookback,
        starting_equity=starting_equity,
    )
