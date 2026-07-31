import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

from Utilities.MarketData.provider import get_market_history
from Utilities.Reporting.constants import (
    DEFAULT_REPORTING_PERIOD,
)
from Utilities.Reporting.reporting_windows import (
    get_reporting_window,
)
from EasyMode.RSI_PriceSolver.Indicator.rsi_calculator import calculate_rsi
from EasyMode.RSI_PriceSolver.performance.annual_returns import (
    build_annual_returns,
)
from Utilities.Performance.build_annual_table import (
    build_annual_table,
)

from Library.Trading.trade_engine import Trade
from Library.Trading.trade_metrics import calculate_trade_metrics

from Library.Trading.portfolio_simulator import PortfolioSimulator
from analytics.campaign.engine import Campaign
from analytics.campaign.campaign_metrics import (
    build_campaign_metrics,
)

DEFAULT_RSI_LENGTH = 3
DEFAULT_THRESHOLD = 28

def build_ulcershield_trades(
    signals,
    starting_equity=100000.0,
):
    trades = []
    positions = {}

    for signal in signals:

        sleeve = signal["sleeve"]
        price = float(signal["price"])
        date = signal["date"]

        if signal["signal"] == "BUY":

            allocation = starting_equity * 0.20
            shares = allocation / price

            positions[sleeve] = {
                "entry_date": date,
                "entry_price": price,
                "shares": shares,
            }

        elif signal["signal"] == "SELL":

            if sleeve not in positions:
                continue

            pos = positions.pop(sleeve)

            pnl = (
                price - pos["entry_price"]
            ) * pos["shares"]

            trades.append(
                Trade(
                    entry_date=pos["entry_date"],
                    exit_date=date,
                    entry_price=pos["entry_price"],
                    exit_price=price,
                    shares=pos["shares"],
                    pnl=pnl,
                    return_pct=(
                        price / pos["entry_price"] - 1
                    ),
                    days_held=(
                        date - pos["entry_date"]
                    ).days,
                    winning_trade=pnl > 0,
                )
            )

    return trades


def build_ulcershield_campaigns(
    daily_states,
    starting_equity,
):
    campaigns = []

    active = False
    start_date = None
    start_equity = starting_equity
    closed_equity = starting_equity
    bars = 0

    for state in daily_states:

        date = state["date"]
        equity = state["equity"]
        active_sleeves = state["active_sleeves"]

        portfolio_active = active_sleeves > 0

        if portfolio_active and not active:
            active = True
            start_date = date
            start_equity = closed_equity
            bars = 0

        if active:
            bars += 1

        if active and not portfolio_active:

            closed_equity = equity

            ret = (
                closed_equity
                / start_equity
                - 1
            )

            campaigns.append(
                Campaign(
                    start_date=start_date,
                    end_date=date,
                    start_equity=start_equity,
                    end_equity=closed_equity,
                    return_pct=ret,
                    bars_held=bars,
                    winning_trade=ret > 0,
                )
            )

            active = False
            start_date = None
            bars = 0

    return campaigns


def build_rsi_pricesolver(
    ticker="TQQQ",
    rsi_length=DEFAULT_RSI_LENGTH,
    threshold=DEFAULT_THRESHOLD,
    period: str = DEFAULT_REPORTING_PERIOD,
    starting_equity=100000.0,
):
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

    if start_date is not None:
        history = full_history[
            (full_history.index >= start_date)
            &
            (full_history.index <= end_date)
        ]
    else:
        history = full_history

    closes = history["close"]

    rsi = calculate_rsi(
        full_history["close"],
        rsi_length,
    )

    signals = []

    position = False

    for date, close in closes.items():

        value = rsi.loc[date]

        if pd.isna(value):
            continue

        if not position and value < threshold:

            signals.append({
                "date": date,
                "signal": "BUY",
                "price": float(close),
                "sleeve": 0,
            })

            position = True

        elif position and value > threshold:

            signals.append({
                "date": date,
                "signal": "SELL",
                "price": float(close),
                "sleeve": 0,
            })

            position = False

    if start_date is not None:

        report_signals = [
            signal
            for signal in signals
            if start_date <= signal["date"] <= end_date
        ]

    else:

        report_signals = signals

    simulator = PortfolioSimulator(
        sleeve_count=1,
        allocation_pct=1.0,
        starting_equity=starting_equity,
    )

    signal_map = {}

    for signal in signals:
        signal_map.setdefault(
            signal["date"],
            [],
        ).append(signal)

    for date, close in closes.items():

        if date in signal_map:

            for signal in signal_map[date]:

                if signal["signal"] == "BUY":
                    simulator.buy(
                        signal["sleeve"],
                        date,
                        signal["price"],
                    )
                else:
                    simulator.sell(
                        signal["sleeve"],
                        signal["price"],
                    )

        simulator.update_day(
            date,
            float(close),
        )

    result = simulator.results()

    trades = build_ulcershield_trades(
        report_signals,
        starting_equity=starting_equity,
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

    closed_equity = [
        day["closed_equity"]
        for day in result["daily_states"]
    ]

    campaigns = build_ulcershield_campaigns(
        result["daily_states"],
        starting_equity,
    )

    campaign_metrics = build_campaign_metrics(
        campaigns,
    )

    print(f"Trades: {len(trade_result['trades'])}")
    print(f"Signals: {len(signals)}")
    print(f"Start: {report_history.index[0]}")
    print(f"End: {report_history.index[-1]}")

    return {
        "ticker": ticker,
        "starting_equity": starting_equity,
        "ending_equity": result["ending_equity"],
        "equity_curve": result["equity_curve"],
        "equity_dates": result["equity_dates"],
        "closed_equity": closed_equity,
        "trade_metrics": trade_metrics,
        "campaign_metrics": campaign_metrics,
        "annual_returns": annual_returns,
        "annual_table": annual_table,
        "start_date": history.index[0],
        "end_date": history.index[-1],
        "trades": trades,
        "signals": signals,
        "campaigns": campaigns,
        "daily_states": result["daily_states"],
        "rsi_length": rsi_length,
        "threshold": threshold,
        "period": period,
    }