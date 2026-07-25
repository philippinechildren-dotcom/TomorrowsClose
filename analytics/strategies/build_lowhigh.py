import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

from market_data.provider import (
    get_market_history,
)

from analytics.common.constants import (
    DEFAULT_REPORTING_PERIOD,
)

from analytics.common.equity_curve import (
    build_strategy_equity_curve,
)

from analytics.common.reporting_windows import (
    get_reporting_window,
)

from analytics.trade.engine import (
    build_trades,
)

from analytics.campaign.metrics import (
    build_trade_metrics,
)


def build_lowhigh(
    ticker: str = "QLD",
    entry_lookback: int = 3,
    exit_lookback: int = 1,
    period: str = DEFAULT_REPORTING_PERIOD,
    starting_equity: float = 100000.0,
) -> dict:
    """
    Build LowHigh mean reversion strategy.
    """

    today = datetime.now(
        ZoneInfo("America/New_York")
    )

    start_date, end_date = get_reporting_window(
        today,
        period,
    )

    history = get_market_history(
        ticker,
        bars=5000,
    )

    if start_date is not None:

        history = history[
            (history.index >= start_date)
            &
            (history.index <= end_date)
        ]

    closes = history["close"]

    signals = []

    position = False

    warmup = max(
        entry_lookback,
        exit_lookback,
    )

    for i in range(warmup, len(history)):

        date = history.index[i]

        close = float(
            history["close"].iloc[i]
        )

        previous_low = (
            history["low"]
            .iloc[
                i-entry_lookback:i
            ]
            .min()
        )

        previous_high = (
            history["high"]
            .iloc[
                i-exit_lookback:i
            ]
            .max()
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

    trade_result = build_trades(
        signals,
        starting_equity=starting_equity,
    )

    trade_metrics = build_trade_metrics(
        trade_result["trades"]
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

        "closed_equity": trade_result["closed_equity"],

        "trade_metrics": trade_metrics,

        "start_date": history.index[0],

        "end_date": history.index[-1],

        "trades": trade_result["trades"],

        "signals": signals,

        "entry_lookback": entry_lookback,

        "exit_lookback": exit_lookback,

        "period": period,

    }