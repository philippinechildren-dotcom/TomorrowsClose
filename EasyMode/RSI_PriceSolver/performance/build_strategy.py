import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

from market_data.provider import get_market_history
from Utilities.Reporting.constants import (
    DEFAULT_REPORTING_PERIOD,
)
from Utilities.Reporting.reporting_windows import (
    get_reporting_window,
)
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
from indicators.rsi_calculator import calculate_rsi

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

    history = full_history

    if start_date is not None:
        history = history[
            (history.index >= start_date)
            &
            (history.index <= end_date)
        ]

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

        if not position and value < threshold:
            signals.append(
                {
                    "date": date,
                    "signal": "BUY",
                    "price": float(close),
                }
            )
            position = True

        elif position and value > threshold:
            signals.append(
                {
                    "date": date,
                    "signal": "SELL",
                    "price": float(close),
                }
            )
            position = False

    if start_date is not None:
        report_signals = [
            s for s in signals
            if start_date <= s["date"] <= end_date
        ]
    else:
        report_signals = signals

    closes = history["close"]

    trade_result = build_trades(
        report_signals,
        starting_equity=starting_equity,
    )

    trade_metrics = calculate_trade_metrics(
        trade_result["trades"]
    )

    equity_result = calculate_strategy_equity_curve(
        closes=closes,
        signals=report_signals,
        starting_equity=starting_equity,
    )

    full_equity_result = calculate_strategy_equity_curve(
        closes=full_history["close"],
        signals=signals,
        starting_equity=starting_equity,
    )

    annual_table = calculate_annual_table(
        trades=build_trades(
            signals,
            starting_equity=starting_equity,
        )["trades"],
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
        "start_date": history.index[0],
        "end_date": history.index[-1],
        "trades": trade_result["trades"],
        "signals": report_signals,
        "rsi_length": rsi_length,
        "threshold": threshold,
        "period": period,
    }