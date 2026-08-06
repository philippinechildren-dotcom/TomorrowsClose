"""
StrategyLab/Strategies/ulcershield.py
"""

from Utilities.market_data import (
    get_market_history,
    filter_history,
)

from Library.Indicators.rsi import calculate_rsi
from Library.Trading.trade_engine import build_trades
from StrategyLab.Metrics.metrics import build_metrics


def build_ulcershield(
    history,
    starting_equity=100000.0,
):
    """
    Build UlcerShield strategy statistics.
    """

    if history.empty:
        return None

    # ==========================================================
    # UlcerShield Systems
    # ==========================================================

    rsi_systems = [
        (1, 2, 28),
        (2, 3, 28),
        (3, 5, 28),
        (4, 8, 28),
        (5, 13, 32),
    ]

    allocation = starting_equity / len(rsi_systems)

    system_results = []

    # ==========================================================
    # Build Each RSI System
    # ==========================================================

    for strategy_number, rsi_length, rsi_threshold in rsi_systems:

        rsi = calculate_rsi(
            history["close"],
            period=rsi_length,
        )

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
                    "strategy_number": strategy_number,
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
                    "strategy_number": strategy_number,
                })

                in_position = False

        # ==========================================================
        # Trades
        # ==========================================================

        trade_results = build_trades(
            signals=signals,
            starting_equity=allocation,
        )

        trades = trade_results["trades"]

        # ==========================================================
        # Daily Equity Curve
        # ==========================================================

        equity_curve = []
        equity = allocation
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

        system_results.append(
            {
                "strategy_number": strategy_number,
                "trades": trades,
                "equity_curve": equity_curve,
            }
        )

    # ==========================================================
    # Combine Equity Curves
    # ==========================================================

    equity_curve = []

    all_trades = []

    number_of_days = len(
        system_results[0]["equity_curve"]
    )

    for day in range(number_of_days):

        equity = 0.0

        for system in system_results:

            equity += system["equity_curve"][day]

        equity_curve.append(equity)

    for system in system_results:

        all_trades.extend(
            system["trades"]
        )

    ending_equity = equity_curve[-1]

    years = (
        (history.index[-1] - history.index[0]).days
        / 365.25
    )

    # ==========================================================
    # Exposure
    # ==========================================================

    total_days = len(history)

    days_in_market = sum(
        trade.days_held
        for trade in all_trades
        if trade.strategy_number == 1
        # ==========================================================
        # Exposure
        # ==========================================================
        #
        # UlcerShield exposure is approximated using RSI System #1
        # (RSI period 2). This system normally enters first and exits
        # with the rest of the portfolio, making it a good proxy for
        # overall portfolio exposure without implementing campaign-
        # level exposure tracking.
    )

    exposure = (
        days_in_market / total_days
    ) if total_days > 0 else 0.0

    # ==========================================================
    # Metrics
    # ==========================================================

    metrics = build_metrics(
        equity_curve=equity_curve,
        trades=all_trades,
        starting_equity=starting_equity,
        ending_equity=ending_equity,
        years=years,
        exposure=exposure,
    )

    # ==========================================================
    # Strategy
    # ==========================================================

    return {
        "name": "UlcerShield",
        "type": "strategy",
        "starting_equity": starting_equity,
        "ending_equity": ending_equity,
        "history": history,
        "equity_curve": equity_curve,
        "years": years,
        "metrics": metrics,
    }


def build_result(
    ticker="TQQQ",
    period=None,
    starting_equity=100000.0,
):
    """
    Build a complete UlcerShield strategy using current market data.
    """

    history = get_market_history(
        ticker=ticker,
    )

    history = filter_history(
        history,
        period,
    )

    return build_ulcershield(
        history=history,
        starting_equity=starting_equity,
    )