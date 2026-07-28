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

from analytics.common.equity_curve import build_strategy_equity_curve
from Library.Trading.trade_engine import build_trades
from analytics.campaign.metrics import build_trade_metrics
from analytics.performance.build_annual_table import build_annual_table


def build_lowhigh_qqq(
    ticker: str = "QQQ",
    entry_lookback: int = 3,
    exit_lookback: int = 1,
    period: str = DEFAULT_REPORTING_PERIOD,
    starting_equity: float = 100000.0,
) -> dict:

    today = datetime.now(ZoneInfo("America/New_York"))
    start_date, end_date = get_reporting_window(today, period)

    full_history = get_market_history(ticker, bars=5000)

    history = full_history
    if start_date is not None:
        history = history[
            (history.index >= start_date)
            & (history.index <= end_date)
        ]

    signals = []
    position = False
    warmup = max(entry_lookback, exit_lookback)

    for i in range(warmup, len(full_history)):
        date = full_history.index[i]
        close = float(full_history["close"].iloc[i])

        previous_low = full_history["low"].iloc[i-entry_lookback:i].min()
        previous_high = full_history["high"].iloc[i-exit_lookback:i].max()

        if not position:
            if close < previous_low:
                signals.append({
                    "date": date,
                    "signal": "BUY",
                    "price": close,
                })
                position = True
        else:
            if close > previous_high:
                signals.append({
                    "date": date,
                    "signal": "SELL",
                    "price": close,
                })
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

    trade_metrics = build_trade_metrics(
        trade_result["trades"]
    )

    equity_result = build_strategy_equity_curve(
        closes=closes,
        signals=report_signals,
        starting_equity=starting_equity,
    )

    full_equity_result = build_strategy_equity_curve(
        closes=full_history["close"],
        signals=signals,
        starting_equity=starting_equity,
    )

    annual_table = build_annual_table(
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
        "entry_lookback": entry_lookback,
        "exit_lookback": exit_lookback,
        "period": period,
    }