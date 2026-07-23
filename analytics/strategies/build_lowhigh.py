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



def build_lowhigh(
    ticker: str = "QLD",
    lookback: int = 3,
    starting_equity: float = 100000.0,
) -> dict:
    """
    Build LowHigh mean reversion strategy.

    Rules:

    Entry:
        Close below previous N-day low

    Exit:
        Close above previous day high

    Execution:
        End-of-day close

    Position:
        100% equity
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


    signals = []

    position = False


    for i in range(lookback, len(history)):

        date = history.index[i]

        close = float(
            history["close"].iloc[i]
        )


        previous_low = (
            history["low"]
            .iloc[i-lookback:i]
            .min()
        )


        previous_high = (
            history["high"]
            .iloc[i-1]
        )


        if not position:

            if close < previous_low:

                signals.append(

                    {
                        "date": date,

                        "signal": "BUY",

                        "price": close,

                    }

                )

                position = True



        else:

            if close > previous_high:

                signals.append(

                    {
                        "date": date,

                        "signal": "SELL",

                        "price": close,

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

        "lookback": lookback,

    }