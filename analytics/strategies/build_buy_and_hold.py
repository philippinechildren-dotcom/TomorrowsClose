from datetime import datetime
from zoneinfo import ZoneInfo

from analytics.common.equity_curve import (
    build_buy_and_hold_equity_curve,
)

from analytics.common.reporting_windows import (
    rolling_one_year,
)

from market_data.provider import (
    get_market_history,
)


def build_buy_and_hold(
    ticker: str,
    starting_equity: float = 100000.0,
) -> dict:
    """
    Build Buy & Hold strategy result.
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

    equity_result = build_buy_and_hold_equity_curve(
        closes=closes,
        starting_equity=starting_equity,
    )

    return {
        "ticker": ticker,

        "starting_equity": equity_result["starting_equity"],

        "ending_equity": equity_result["ending_equity"],

        "equity_curve": equity_result["equity_curve"],

        "shares": equity_result["shares"],

        "start_date": history.index[0],

        "end_date": history.index[-1],
    }