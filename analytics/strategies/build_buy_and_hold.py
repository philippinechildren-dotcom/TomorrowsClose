from datetime import datetime
from zoneinfo import ZoneInfo

from analytics.common.constants import (
    DEFAULT_REPORTING_PERIOD,
)

from analytics.common.equity_curve import (
    build_buy_and_hold_equity_curve,
)

from analytics.common.reporting_windows import (
    get_reporting_window,
)

from market_data.provider import (
    get_market_history,
)

from analytics.performance.build_annual_table import (
    build_annual_table,
)


def build_buy_and_hold(
    ticker: str,
    period: str = DEFAULT_REPORTING_PERIOD,
    starting_equity: float = 100000.0,
) -> dict:
    """
    Build Buy & Hold strategy result.
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
    )

    if start_date is not None:

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

    annual_table = build_annual_table(
        trades=[],
        equity_curve=equity_result["equity_curve"],
        equity_dates=equity_result["equity_dates"],
    )

    return {

        "ticker": ticker,

        "starting_equity": equity_result["starting_equity"],

        "ending_equity": equity_result["ending_equity"],

        "equity_curve": equity_result["equity_curve"],

        "equity_dates": equity_result["equity_dates"],

        "annual_table": annual_table,

        "shares": equity_result["shares"],

        "start_date": history.index[0],

        "end_date": history.index[-1],

        "period": period,

    }