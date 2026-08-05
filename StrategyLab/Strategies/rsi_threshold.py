"""
StrategyLab/Strategies/rsi_threshold.py
"""

from Utilities.market_data import get_market_history
from Library.Indicators.rsi import calculate_rsi
from Library.Trading.trade_engine import build_trades
from StrategyLab.Metrics.metrics import build_metrics


def build_rsi_threshold(
    history,
    rsi_length=3,
    rsi_threshold=28,
    starting_equity=100000.0,
):
    """
    Build RSI Threshold strategy statistics.
    """

    if history.empty:
        return None

    # ==========================================================
    # RSI
    # ==========================================================

    rsi = calculate_rsi(
        history["close"],
        period=rsi_length,
    )

    # ==========================================================
    # Signals
    # ==========================================================

    signals = []
    in_position = False

    for date, row in history.iterrows():

        close = float(row["close"])
        current_rsi = rsi.loc[date]

        if current_rsi != current_rsi:
            continue

        if (
            not in_position
            and current_rsi < rsi_threshold
        ):

            signals.append({
                "date": date,
                "signal": "BUY",
                "price": close,
            })

            in_position = True

        elif (
            in_position
            and current_rsi > rsi_threshold
        ):

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
            shares = equity / trades[trade_number].entry_price
            in_position = True

        equity_curve.append(
            shares * close if in_position else equity
        )

        if (
            trade_number < len(trades)
            and date == trades[trade_number].exit_date
        ):
            equity = shares * trades[trade_number].exit_price
            in_position = False
            trade_number += 1

    ending_equity = equity_curve[-1]

    years = (
        (history.index[-1] - history.index[0]).days
        / 365.25
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
        exposure=1.0,
    )

    # ==========================================================
    # Strategy
    # ==========================================================

    return {
        "name": "RSI Threshold",
        "type": "strategy",
        "starting_equity": starting_equity,
        "ending_equity": ending_equity,
        "equity_curve": equity_curve,
        "years": years,
        "metrics": metrics,
    }


def build_result(
    ticker="TQQQ",
    rsi_length=3,
    rsi_threshold=28,
    starting_equity=100000.0,
):
    """
    Build a complete RSI Threshold strategy using current market data.
    """

    history = get_market_history(
        ticker=ticker,
    )

    return build_rsi_threshold(
        history=history,
        rsi_length=rsi_length,
        rsi_threshold=rsi_threshold,
        starting_equity=starting_equity,
    )