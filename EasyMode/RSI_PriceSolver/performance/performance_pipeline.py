import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

from Utilities.MarketData.provider import get_market_history
from Utilities.Reporting.constants import DEFAULT_REPORTING_PERIOD
from Utilities.Reporting.reporting_windows import get_reporting_window

from EasyMode.RSI_PriceSolver.Indicator.rsi_calculator import calculate_rsi

from EasyMode.RSI_PriceSolver.performance.equity_curve import (
    calculate_strategy_equity_curve,
)
from EasyMode.RSI_PriceSolver.performance.trade_history import (
    calculate_trade_history,
)
from EasyMode.RSI_PriceSolver.performance.trade_metrics import (
    calculate_trade_metrics,
)
from EasyMode.RSI_PriceSolver.performance.annual_table import (
    calculate_annual_table,
)


def build_rsi_pricesolver(
    ticker: str = "TQQQ",
    rsi_length: int = 3,
    threshold: float = 28,
    period: str = DEFAULT_REPORTING_PERIOD,
    starting_equity: float = 100000.0,
) -> dict:

    today = datetime.now(
        ZoneInfo("America/New_York")
    )

    start_date, end_date = get_reporting_window(
        today,
        period,
    )

    full_history = get_market_history(
        ticker,
    )

    rsi = calculate_rsi(
        full_history["close"],
        rsi_length,
    )

    signals = []

    position = False

    for date, close in full_history["close"].items():

        value = rsi.loc[date]

        if pd.isna(value):
            continue

        if (not position) and value < threshold:

            signals.append({
                "date": date,
                "signal": "BUY",
                "price": float(close),
            })

            position = True

        elif position and value > threshold:

            signals.append({
                "date": date,
                "signal": "SELL",
                "price": float(close),
            })

            position = False

    report_history = full_history

    if start_date is not None:

        report_history = report_history[
            (report_history.index >= start_date)
            &
            (report_history.index <= end_date)
        ]

    report_signals = []

    if start_date is None:

        report_signals = signals

        initial_position = False
        initial_shares = 0.0
        initial_cash = starting_equity

    else:

        equity = starting_equity
        shares = 0.0
        in_position = False

        for signal in signals:

            if signal["date"] >= start_date:
                break

            price = signal["price"]

            if signal["signal"] == "BUY":

                shares = equity / price
                equity = 0.0
                in_position = True

            else:

                equity = shares * price
                shares = 0.0
                in_position = False

        initial_position = in_position
        initial_shares = shares
        initial_cash = equity

        report_signals = [
            s
            for s in signals
            if start_date <= s["date"] <= end_date
        ]

    trade_result = calculate_trade_history(
        report_signals,
        starting_equity=starting_equity,
    )

    trade_metrics = calculate_trade_metrics(
        trade_result["trades"],
    )

    equity_result = calculate_strategy_equity_curve(
        closes=report_history["close"],
        signals=report_signals,
        starting_equity=starting_equity,
        initial_position=initial_position,
        initial_shares=initial_shares,
        initial_cash=initial_cash,
    )

    full_trade_result = calculate_trade_history(
        signals,
        starting_equity=starting_equity,
    )

    full_equity_result = calculate_strategy_equity_curve(
        closes=full_history["close"],
        signals=signals,
        starting_equity=starting_equity,
    )

    annual_table = calculate_annual_table(
        trades=full_trade_result["trades"],
        equity_curve=full_equity_result["equity_curve"],
        equity_dates=full_equity_result["equity_dates"],
    )

    return {
        "ticker": ticker,
        "starting_equity": starting_equity,
        "ending_equity": equity_result["ending_equity"],
        "equity_curve": equity_result["equity_curve"],
        "equity_dates": equity_result["equity_dates"],
        "closed_equity": trade_result["closed_equity"],
        "trade_metrics": trade_metrics,
        "annual_table": annual_table,
        "start_date": report_history.index[0],
        "end_date": report_history.index[-1],
        "trades": trade_result["trades"],
        "signals": report_signals,
        "rsi_length": rsi_length,
        "threshold": threshold,
        "period": period,
    }