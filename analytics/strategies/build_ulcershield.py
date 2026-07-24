import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

from market_data.provider import get_market_history

from analytics.common.reporting_windows import rolling_one_year
from analytics.strategies.build_rsi_pricesolver import calculate_rsi
from analytics.trade.engine import Trade
from analytics.portfolio.engine import PortfolioEngine
from analytics.campaign.engine import Campaign


DEFAULT_RSI_LENGTHS = [2,3,5,8,13]
DEFAULT_THRESHOLDS = [28,28,28,28,32]


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
                    return_pct=price / pos["entry_price"] - 1,
                    days_held=(date-pos["entry_date"]).days,
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
                closed_equity / start_equity
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
                    winning_campaign=ret > 0,
                )
            )

            active = False
            start_date = None
            bars = 0

    return campaigns


def build_ulcershield(
    ticker="TQQQ",
    rsi_lengths=None,
    thresholds=None,
    starting_equity=100000.0,
):
    if rsi_lengths is None:
        rsi_lengths = DEFAULT_RSI_LENGTHS

    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS

    today = datetime.now(
        ZoneInfo("America/New_York")
    )

    start_date,end_date = rolling_one_year(today)

    full_history = get_market_history(
        ticker,
        bars=1000,
    )

    history = full_history[
        (full_history.index >= start_date)
        &
        (full_history.index <= end_date)
    ]

    closes = history["close"]

    rsi_values = []

    for length in rsi_lengths:
        rsi_values.append(
            calculate_rsi(
                full_history["close"],
                length,
            )
        )

    signals = []

    positions = {
        i: False
        for i in range(len(rsi_lengths))
    }

    for date, close in closes.items():

        for sleeve,length in enumerate(rsi_lengths):

            value = rsi_values[sleeve].loc[date]

            if pd.isna(value):
                continue

            threshold = thresholds[sleeve]

            if not positions[sleeve] and value < threshold:

                signals.append(
                    {
                        "date": date,
                        "signal": "BUY",
                        "price": float(close),
                        "sleeve": sleeve,
                    }
                )

                positions[sleeve] = True

            elif positions[sleeve] and value > threshold:

                signals.append(
                    {
                        "date": date,
                        "signal": "SELL",
                        "price": float(close),
                        "sleeve": sleeve,
                    }
                )

                positions[sleeve] = False


    engine = PortfolioEngine(
        sleeve_count=5,
        allocation_pct=0.20,
        starting_equity=starting_equity,
    )

    signal_map = {}

    for signal in signals:
        signal_map.setdefault(
            signal["date"],
            []
        ).append(signal)


    for date, close in closes.items():

        if date in signal_map:
            for signal in signal_map[date]:

                if signal["signal"] == "BUY":
                    engine.buy(
                        signal["sleeve"],
                        date,
                        signal["price"],
                    )

                else:
                    engine.sell(
                        signal["sleeve"],
                        signal["price"],
                    )

        engine.update_day(
            date,
            float(close),
        )


    result = engine.results()

    trades = build_ulcershield_trades(
        signals,
        starting_equity,
    )

    closed_equity = [
        day["closed_equity"]
        for day in result["daily_states"]
    ]

    campaigns = build_ulcershield_campaigns(
        result["daily_states"],
        starting_equity,
    )

    return {
        "ticker": ticker,
        "starting_equity": starting_equity,
        "ending_equity": result["ending_equity"],
        "equity_curve": result["equity_curve"],
        "start_date": history.index[0],
        "end_date": history.index[-1],
        "trades": trades,
        "signals": signals,
        "campaigns": campaigns,
        "closed_equity": closed_equity,
        "daily_states": result["daily_states"],
        "rsi_lengths": rsi_lengths,
        "thresholds": thresholds,
    }