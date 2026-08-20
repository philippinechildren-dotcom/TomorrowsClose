from types import SimpleNamespace
from Utilities.market_data import (
    get_market_history,
    filter_history,
)
from StrategyLab.Metrics.metrics import build_metrics


def build_lowhigh_ulcershield(
    history,
    entry_lookback=1,
    exit_lookback=1,
    starting_equity=100000.0,
):
    """
    LowHigh UlcerShield strategy backtest (5 tranches of 20% allocation).

    PineScript Logic:
        lowestLow   = ta.lowest(low[1], xDays)
        highestHigh = ta.highest(high[1], yDays)

        buyCondition  = close < lowestLow
        exitCondition = close > highestHigh
    """
    if history.empty:
        return None

    max_pyramids = 5
    entry_percent = 0.20

    # ==========================================================
    # LOOKBACK CALCULATIONS (Excludes current bar)
    # ==========================================================
    lowest_low = (
        history["low"]
        .shift(1)
        .rolling(
            window=entry_lookback,
            min_periods=entry_lookback,
        )
        .min()
    )

    highest_high = (
        history["high"]
        .shift(1)
        .rolling(
            window=exit_lookback,
            min_periods=exit_lookback,
        )
        .max()
    )

    # ==========================================================
    # ACCOUNT STATE
    # ==========================================================
    cash = float(starting_equity)
    positions = []
    trades = []
    trade_number = 0
    equity_curve = []

    # ==========================================================
    # DAILY BAR LOOP
    # ==========================================================
    for date, row in history.iterrows():
        close = float(row["close"])

        current_lowest_low = lowest_low.loc[date]
        current_highest_high = highest_high.loc[date]

        # Skip bars until lookbacks are populated
        if (
            current_lowest_low != current_lowest_low
            or current_highest_high != current_highest_high
        ):
            position_value = sum(
                position["shares"] * close
                for position in positions
            )
            equity_curve.append(cash + position_value)
            continue

        buy_condition = close < current_lowest_low
        exit_condition = close > current_highest_high

        # ======================================================
        # EXITS
        # ======================================================
        if exit_condition and positions:
            for position in positions:
                exit_value = position["shares"] * close
                cash += exit_value

                trade = position["trade"]
                trade.exit_date = date
                trade.exit_price = close
                trade.days_held = (date - trade.entry_date).days
                trade.return_pct = (close / trade.entry_price) - 1.0

                trade.pnl = exit_value - (position["shares"] * trade.entry_price)
                trade.dollar_return = trade.pnl

                # Fixed: Set winning_trade and losing_trade flags
                trade.winning_trade = trade.return_pct > 0
                trade.losing_trade = trade.return_pct < 0

                trades.append(trade)

            positions = []

        # ======================================================
        # ENTRIES (Pyramiding up to 5 tranches)
        # ======================================================
        if buy_condition and len(positions) < max_pyramids:
            existing_position_value = sum(
                position["shares"] * close
                for position in positions
            )
            current_equity = cash + existing_position_value

            # 20% of current equity per tranche
            entry_value = current_equity * entry_percent
            shares = entry_value / close
            cash -= entry_value

            trade = SimpleNamespace(
                trade_number=trade_number,
                strategy_number=1,
                entry_date=date,
                entry_price=close,
                exit_date=None,
                exit_price=None,
                days_held=0,
                return_pct=0.0,
                pnl=0.0,
                dollar_return=0.0,
                winning_trade=False,
                losing_trade=False,
            )

            trade_number += 1

            positions.append({
                "shares": shares,
                "trade": trade,
            })

        # Track daily mark-to-market equity
        current_position_value = sum(
            position["shares"] * close
            for position in positions
        )
        equity_curve.append(cash + current_position_value)

    # ==========================================================
    # FINAL MARK-TO-MARKET FOR OPEN POSITIONS
    # ==========================================================
    if positions and not history.empty:
        final_date = history.index[-1]
        final_close = float(history.iloc[-1]["close"])

        for position in positions:
            trade = position["trade"]
            trade.exit_date = final_date
            trade.exit_price = final_close
            trade.days_held = (final_date - trade.entry_date).days
            trade.return_pct = (final_close / trade.entry_price) - 1.0

            trade.pnl = (position["shares"] * final_close) - (position["shares"] * trade.entry_price)
            trade.dollar_return = trade.pnl

            # Fixed: Set winning_trade and losing_trade flags
            trade.winning_trade = trade.return_pct > 0
            trade.losing_trade = trade.return_pct < 0

            trades.append(trade)

    ending_equity = equity_curve[-1] if equity_curve else starting_equity
    years = len(history) / 252.0 if len(history) > 0 else 1.0

    # Total days in market across all open position days
    total_days = len(history)
    exposure_days = sum(1 for e in equity_curve if e != starting_equity)
    exposure = exposure_days / total_days if total_days > 0 else 0.0

    metrics = build_metrics(
        equity_curve=equity_curve,
        trades=trades,
        starting_equity=starting_equity,
        ending_equity=ending_equity,
        years=years,
        exposure=exposure,
    )

    return {
        "name": "LowHigh UlcerShield",
        "type": "strategy",
        "starting_equity": starting_equity,
        "ending_equity": ending_equity,
        "history": history,
        "equity_curve": equity_curve,
        "trades": trades,
        "years": years,
        "metrics": metrics,
    }


def build_result(
    ticker="QQQ",
    period=None,
    entry_lookback=1,
    exit_lookback=1,
    starting_equity=100000.0,
):
    """
    Build LowHigh UlcerShield using current market data.
    """
    history = get_market_history(ticker=ticker)
    history = filter_history(history, period)

    return build_lowhigh_ulcershield(
        history=history,
        entry_lookback=entry_lookback,
        exit_lookback=exit_lookback,
        starting_equity=starting_equity,
    )