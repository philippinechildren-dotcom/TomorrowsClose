from typing import List


def calculate_buy_and_hold_equity_curve(
    closes,
    starting_equity: float = 100000.0,
) -> dict:
    """
    Build a daily Buy & Hold equity curve.

    Parameters
    ----------
    closes : pandas.Series
        Daily closing prices.

    starting_equity : float
        Starting account value.

    Returns
    -------
    dict
    """

    if len(closes) == 0:

        return {
            "shares": 0.0,
            "starting_equity": starting_equity,
            "ending_equity": starting_equity,
            "equity_curve": [],
            "equity_dates": [],
        }

    entry_price = float(
        closes.iloc[0]
    )

    shares = (
        starting_equity / entry_price
    )

    equity_curve = []
    equity_dates = []

    for date, close in closes.items():

        equity = (
            shares
            *
            float(close)
        )

        equity_curve.append(
            equity
        )

        equity_dates.append(
            date
        )

    return {

        "shares": shares,

        "starting_equity": starting_equity,

        "ending_equity": equity_curve[-1],

        "equity_curve": equity_curve,

        "equity_dates": equity_dates,

    }

def calculate_strategy_equity_curve(
    closes,
    signals,
    starting_equity: float = 100000.0,
    initial_position: bool = False,
    initial_shares: float = 0.0,
    initial_cash: float | None = None,
) -> dict:
    """
    Build daily mark-to-market strategy equity curve.

    Matches TradingView behavior:

    - 100% of equity invested on entry
    - Positions marked daily
    - Open trades included in drawdowns
    - Cash when flat

    Parameters
    ----------
    closes : pandas.Series

        Daily closing prices.

    signals : list

        BUY / SELL signals with dates and prices.

    Returns
    -------
    dict
    """

    position = initial_position

    shares = initial_shares

    if initial_cash is None:
        cash = starting_equity if not initial_position else 0.0
    else:
        cash = initial_cash

    signal_map = {

        signal["date"]: signal

        for signal in signals

    }

    equity_curve = []
    equity_dates = []

    for date, close in closes.items():

        price = float(close)

        if date in signal_map:

            signal = signal_map[date]

            if signal["signal"] == "BUY":

                shares = (
                    cash / price
                )

                cash = 0.0

                position = True

            elif signal["signal"] == "SELL":

                cash = (
                    shares
                    *
                    price
                )

                shares = 0.0

                position = False

        if shares > 0:

            equity = (
                shares
                *
                price
            )

        else:

            equity = cash

        equity_curve.append(
            equity
        )

        equity_dates.append(
            date
        )

    return {

        "starting_equity": starting_equity,

        "ending_equity": equity_curve[-1]
        if equity_curve
        else starting_equity,

        "equity_curve": equity_curve,

        "equity_dates": equity_dates,

    }