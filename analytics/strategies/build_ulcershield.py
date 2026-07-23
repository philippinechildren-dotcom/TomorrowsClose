import pandas as pd

from analytics.indicators.rsi import rsi
from analytics.portfolio.engine import PortfolioEngine


DEFAULT_RSI_LENGTHS = [2, 3, 5, 8, 13]
DEFAULT_THRESHOLDS = [28, 28, 28, 28, 32]


def build_ulcershield(
    data: pd.DataFrame,
    rsi_lengths=None,
    thresholds=None,
    starting_equity=100000.0,
):

    if rsi_lengths is None:
        rsi_lengths = DEFAULT_RSI_LENGTHS

    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS

    closes = data["close"]

    engine = PortfolioEngine(
        sleeve_count=5,
        allocation_pct=0.20,
        starting_equity=starting_equity,
    )

    # ---------------------------------------------
    # Calculate all RSI series
    # ---------------------------------------------

    rsi_series = []

    for length in rsi_lengths:
        rsi_series.append(
            rsi(closes, length)
        )

    # ---------------------------------------------
    # Walk through each trading day
    # ---------------------------------------------

    for i in range(1, len(data)):

        date = data.index[i]
        close = float(closes.iloc[i])

        # -----------------------------------------
        # Process each sleeve
        # -----------------------------------------

        for sleeve in range(5):

            today = rsi_series[sleeve].iloc[i]
            yesterday = rsi_series[sleeve].iloc[i - 1]

            threshold = thresholds[sleeve]

            # TradingView crossunder()
            buy_signal = (
                yesterday >= threshold
                and
                today < threshold
            )

            # TradingView crossover()
            sell_signal = (
                yesterday <= threshold
                and
                today > threshold
            )

            if buy_signal:
                engine.buy(
                    sleeve_id=sleeve,
                    date=date,
                    price=close,
                )

            elif sell_signal:
                engine.sell(
                    sleeve_id=sleeve,
                    price=close,
                )

        engine.update_day(
            date=date,
            close=close,
        )

    # ---------------------------------------------
    # Portfolio Results
    # ---------------------------------------------

    portfolio = engine.results()

    equity_curve = portfolio["equity_curve"]

    from analytics.common.performance import build_performance
    from analytics.trade.metrics import build_trade_metrics

    performance = build_performance(
        equity_curve=equity_curve,
        start_date=data.index[0],
        end_date=data.index[-1],
        starting_equity=starting_equity,
    )

    trade_metrics = build_trade_metrics(
        equity_curve=equity_curve
    )

    return {
        "starting_equity": performance["starting_equity"],
        "ending_equity": performance["ending_equity"],
        "total_return": performance["total_return"],
        "cagr": performance["cagr"],
        "max_eod_drawdown": performance["max_eod_drawdown"],
        "ulcer_index": performance["ulcer_index"],
        "upi": performance["upi"],
        "years": performance["years"],
        "trade_metrics": trade_metrics,
        "portfolio": portfolio,
        "equity_curve": equity_curve,
        "rsi_lengths": rsi_lengths,
        "thresholds": thresholds,
    }