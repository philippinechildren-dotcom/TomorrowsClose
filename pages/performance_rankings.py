from flask import request

from Other_Strategies.Trend_Following.Buy_and_Hold.performance.build_strategy import (
    build_buy_and_hold,
)
from EasyMode.LowHigh.performance.build_strategy import build_lowhigh
from EasyMode.RSI_PriceSolver.performance.build_strategy import (
    build_rsi_pricesolver,
)
from analytics.strategies.build_ulcershield import build_ulcershield

from analytics.performance.metrics import calculate_performance


def build_result():

    period = request.args.get("period", "1y")

    sort = request.args.get("sort", "upi")

    direction = request.args.get("direction", "desc")

    reverse = direction == "desc"

    rankings = []

    # --------------------------------------------------
    # Buy & Hold
    # --------------------------------------------------

    bh = build_buy_and_hold(
        ticker="QQQ",
        period=period,
    )

    rankings.append({

        "strategy": "Buy & Hold",

        "ticker": bh["ticker"],

        "performance": calculate_performance(
            bh["equity_curve"],
            bh.get("closed_equity"),
        ),

        "trade_metrics": bh.get("trade_metrics"),

    })

    # --------------------------------------------------
    # LowHigh
    # --------------------------------------------------

    lowhigh = build_lowhigh(
        period=period,
    )

    rankings.append({

        "strategy": "LowHigh",

        "ticker": lowhigh["ticker"],

        "performance": calculate_performance(
            lowhigh["equity_curve"],
            lowhigh["closed_equity"],
        ),

        "trade_metrics": lowhigh.get("trade_metrics"),

    })

    # --------------------------------------------------
    # RSI PriceSolver
    # --------------------------------------------------

    rsi = build_rsi_pricesolver(
        period=period,
    )

    rankings.append({

        "strategy": "RSI PriceSolver",

        "ticker": rsi["ticker"],

        "performance": calculate_performance(
            rsi["equity_curve"],
            rsi["closed_equity"],
        ),

        "trade_metrics": rsi.get("trade_metrics"),

    })

    # --------------------------------------------------
    # UlcerShield
    # --------------------------------------------------

    ulcer = build_ulcershield(
        period=period,
    )

    rankings.append({

        "strategy": "UlcerShield",

        "ticker": ulcer["ticker"],

        "performance": calculate_performance(
            ulcer["equity_curve"],
            ulcer["closed_equity"],
        ),

        "trade_metrics": ulcer.get("campaign_metrics"),

    })

    # --------------------------------------------------
    # Sorting
    # --------------------------------------------------

    def sort_value(row):

        performance = row["performance"]

        metrics = row["trade_metrics"]

        if sort in performance:

            value = performance[sort]

            return value if value is not None else 0

        if metrics and sort in metrics:

            value = metrics[sort]

            return value if value is not None else 0

        if sort == "strategy":

            return row["strategy"]

        if sort == "ticker":

            return row["ticker"]

        return 0

    rankings.sort(

        key=sort_value,

        reverse=reverse,

    )

    return {

        "rankings": rankings,

        "period": period,

        "sort": sort,

        "direction": direction,

    }