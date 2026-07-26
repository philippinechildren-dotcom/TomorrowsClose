from datetime import datetime
from zoneinfo import ZoneInfo

from market_data.provider import get_market_history

from analytics.common.constants import DEFAULT_REPORTING_PERIOD
from analytics.common.reporting_windows import get_reporting_window

from analytics.performance.build_annual_returns import (
    build_annual_returns,
)
from analytics.performance.build_annual_table import (
    build_annual_table,
)

from analytics.trade.engine import Trade
from analytics.trade.metrics import calculate_trade_metrics

from analytics.portfolio.engine import PortfolioEngine


def build_buy_and_hold_trades(
    closes,
    starting_equity=100000.0,
):
    first_date = closes.index[0]
    last_date = closes.index[-1]

    entry_price = float(closes.iloc[0])
    exit_price = float(closes.iloc[-1])

    shares = starting_equity / entry_price

    pnl = (
        exit_price - entry_price
    ) * shares

    return [
        Trade(
            entry_date=first_date,
            exit_date=last_date,
            entry_price=entry_price,
            exit_price=exit_price,
            shares=shares,
            pnl=pnl,
            return_pct=(
                exit_price / entry_price - 1
            ),
            days_held=(
                last_date - first_date
            ).days,
            winning_trade=pnl > 0,
        )
    ]


def build_buy_and_hold(
    ticker: str,
    period: str = DEFAULT_REPORTING_PERIOD,
    starting_equity: float = 100000.0,
):
    today = datetime.now(
        ZoneInfo("America/New_York")
    )

    start_date, end_date = get_reporting_window(
        today,
        period,
    )

    history = get_market_history(
        ticker,
    )

    if start_date is not None:
        history = history[
            (history.index >= start_date)
            &
            (history.index <= end_date)
        ]

    closes = history["close"]

    engine = PortfolioEngine(
        sleeve_count=1,
        allocation_pct=1.00,
        starting_equity=starting_equity,
    )

    first_date = closes.index[0]
    first_price = float(closes.iloc[0])

    engine.buy(
        0,
        first_date,
        first_price,
    )

    for date, close in closes.items():
        engine.update_day(
            date,
            float(close),
        )

    result = engine.results()

    trades = build_buy_and_hold_trades(
        closes,
        starting_equity,
    )

    trade_metrics = calculate_trade_metrics(
        trades,
    )

    annual_returns = build_annual_returns(
        trades=trades,
        equity_curve=result["equity_curve"],
        equity_dates=result["equity_dates"],
    )

    annual_table = build_annual_table(
        trades=trades,
        equity_curve=result["equity_curve"],
        equity_dates=result["equity_dates"],
    )

    return {
        "ticker": ticker,
        "starting_equity": starting_equity,
        "ending_equity": result["ending_equity"],
        "equity_curve": result["equity_curve"],
        "equity_dates": result["equity_dates"],
        "trade_metrics": trade_metrics,
        "annual_returns": annual_returns,
        "annual_table": annual_table,
        "trades": trades,
        "start_date": history.index[0],
        "end_date": history.index[-1],
        "period": period,
    }