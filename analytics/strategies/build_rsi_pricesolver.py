import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

from market_data.provider import (
    get_market_history,
)

from analytics.common.equity_curve import (
    build_strategy_equity_curve,
)

from analytics.common.reporting_windows import (
    rolling_one_year,
)

from analytics.trade.engine import (
    build_trades,
)



def calculate_rsi(
    closes: pd.Series,
    length: int = 3,
) -> pd.Series:
    """
    Calculate TradingView-style Wilder RSI.
    """

    delta = closes.diff()

    gain = delta.clip(
        lower=0
    )

    loss = -delta.clip(
        upper=0
    )


    avg_gain = (
        gain
        .ewm(
            alpha=1 / length,
            adjust=False,
        )
        .mean()
    )


    avg_loss = (
        loss
        .ewm(
            alpha=1 / length,
            adjust=False,
        )
        .mean()
    )


    rs = avg_gain / avg_loss


    rsi = 100 - (
        100 /
        (1 + rs)
    )


    return rsi



def build_rsi_pricesolver(
    ticker: str = "TQQQ",
    rsi_length: int = 3,
    threshold: float = 28,
    starting_equity: float = 100000.0,
) -> dict:
    """
    Build RSI PriceSolver strategy results.

    Rules:

    Entry:
        RSI < threshold

    Exit:
        RSI > threshold

    Execution:
        End-of-day close

    Position:
        100% of current equity
    """


    today = datetime.now(
        ZoneInfo("America/New_York")
    )


    start_date, end_date = rolling_one_year(
        today
    )


    history = get_market_history(
        ticker,
        bars=500,
    )


    history = history[
        (history.index >= start_date)
        &
        (history.index <= end_date)
    ]


    closes = history["close"]


    rsi = calculate_rsi(
        closes,
        rsi_length,
    )


    signals = []

    position = False


    for date, close in closes.items():

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



    trades = build_trades(
        signals,
        starting_equity=starting_equity,
    )



    equity_result = build_strategy_equity_curve(

        closes=closes,

        signals=signals,

        starting_equity=starting_equity,

    )


    return {

        "ticker": ticker,

        "starting_equity": starting_equity,

        "ending_equity": equity_result["ending_equity"],

        "equity_curve": equity_result["equity_curve"],

        "start_date": history.index[0],

        "end_date": history.index[-1],

        "trades": trades,

        "signals": signals,

        "rsi_length": rsi_length,

        "threshold": threshold,

    }