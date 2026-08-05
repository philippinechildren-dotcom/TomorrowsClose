"""
StrategyLab/Strategies/lowhigh.py
"""

from Utilities.market_data import (
    get_market_history,
    filter_history,
)

from Library.Indicators.donchian import calculate_donchian
from Library.Trading.trade_engine import build_trades
from StrategyLab.Metrics.metrics import build_metrics


def build_lowhigh(
    history,
    entry_lookback=3,
    exit_lookback=1,
    starting_equity=100000.0,
):
    """
    Build LowHigh strategy statistics.
    """

    if history.empty:
        return None

    # ==========================================================
    # Donchian Levels
    # ==========================================================

    upper_band, lower_band = calculate_donchian(
        history["high"],
        history["low"],
        upper_lookback=exit_lookback,
        lower_lookback=entry_lookback,
    )

    # ==========================================================
    # Signals
    # ==========================================================

    signals = []
    in_position = False

    for date, row in history.iterrows():

        close = float(row["close"])

        if (
            not in_position
            and close < lower_band.loc[date]
        ):

            signals.append({
                "date": date,
                "signal": "BUY",
                "price": close,
            })

            in_position = True

        elif (
            in_position
            and close > upper_band.loc[date]
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
        "name": "LowHigh",
        "type": "strategy",
        "starting_equity": starting_equity,
        "ending_equity": ending_equity,
        "equity_curve": equity_curve,
        "years": years,
        "metrics": metrics,
    }


def build_result(
    ticker="QLD",
    period=None,
    entry_lookback=3,
    exit_lookback=1,
    starting_equity=100000.0,
):
    """
    Build a complete LowHigh strategy using current market data.
    """

    history = get_market_history(
        ticker=ticker,
    )

    history = filter_history(
        history,
        period,
    )

    return build_lowhigh(
        history=history,
        entry_lookback=entry_lookback,
        exit_lookback=exit_lookback,
        starting_equity=starting_equity,
    )