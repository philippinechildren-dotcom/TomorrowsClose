from datetime import datetime
from zoneinfo import ZoneInfo
from market_data.provider import get_market_history
from Utilities.Reporting.constants import (
    DEFAULT_REPORTING_PERIOD,
)
from Utilities.Reporting.reporting_windows import (
    get_reporting_window,
)
from EasyMode.RSI_PriceSolver.performance.annual_returns import (
    build_annual_returns,
)
from EasyMode.RSI_PriceSolver.performance.annual_table import (
    calculate_annual_table,
)
from Library.Trading.trade_engine import Trade
from Library.Trading.trade_metrics import calculate_trade_metrics
from Library.Trading.portfolio_simulator import PortfolioSimulator

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

    simulator = PortfolioSimulator(
        sleeve_count=1,
        allocation_pct=1.00,
        starting_equity=starting_equity,
    )

    first_date = closes.index[0]
    first_price = float(closes.iloc[0])

    simulator.buy(
        0,
        first_date,
        first_price,
    )

    for date, close in closes.items():
        simulator.update_day(
            date,
            float(close),
        )

    result = simulator.results()

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

    annual_table = calculate_annual_table(
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