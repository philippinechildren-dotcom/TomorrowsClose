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
    period: str = DEFAULT_REPORTING_PERIOD,
    starting_equity: float = 100000.0,
) -> dict:
    """
    Build RSI PriceSolver strategy results.
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

        "rsi_length": rsi_length,

        "threshold": threshold,

        "period": period,

    }