"""
Rankings/build_rankings_json.py
"""

import json
from pathlib import Path
from datetime import datetime

from StrategyLab.Benchmarks.buy_and_hold import (
    build_result as build_buy_and_hold_result,
)

from StrategyLab.Strategies.lowhigh import (
    build_result as build_lowhigh_result,
)

from StrategyLab.Strategies.rsi_threshold import (
    build_result as build_rsi_threshold_result,
)

from StrategyLab.Strategies.ulcershield import (
    build_result as build_ulcershield_result,
)

from Rankings.rankings import build_rankings


TIME_PERIODS = [
    ("maximum", None),
    ("10_year", "10_years"),
    ("5_year", "5_years"),
    ("3_year", "3_years"),
    ("1_year", "1_year"),
    ("ytd", "ytd"),
    ("6_month", "6_months"),
    ("3_month", "3_months"),
    ("1_month", "1_month"),
]

def build_rankings_json():

    rankings_json = {
        "updated": datetime.today().strftime("%Y-%m-%d"),
    }

    for period_name, period in TIME_PERIODS:

        buy_and_hold = build_buy_and_hold_result(
            period=period,
        )

        lowhigh = build_lowhigh_result(
            period=period,
        )

        rsi_threshold = build_rsi_threshold_result(
            period=period,
        )

        ulcershield = build_ulcershield_result(
            period=period,
        )

        rankings = build_rankings(
            [
                buy_and_hold,
                lowhigh,
                rsi_threshold,
                ulcershield,
            ],
            rank_by="ulcer_performance_index",
        )

        rankings_json[period_name] = []

        for result in rankings:

            metrics = result["metrics"]

            rankings_json[period_name].append(
                {
                    "rank": result["rank"],
                    "name": result["name"],
                    "cagr": metrics["cagr"],
                    "max_eod_drawdown": metrics["max_eod_drawdown"],
                    "max_closed_trade_drawdown": metrics["max_closed_trade_drawdown"],
                    "ulcer_index": metrics["ulcer_index"],
                    "ulcer_performance_index": metrics["ulcer_performance_index"],
                    "calmar_ratio": metrics["calmar_ratio"],
                    "number_of_trades": metrics["number_of_trades"],
                    "trades_per_year": metrics["trades_per_year"],
                    "win_rate": metrics["win_rate"],
                    "profit_factor": metrics["profit_factor"],
                    "expectancy_percent": metrics["expectancy_percent"],
                }
            )

    output_file = (
        Path(__file__).parent
        / "rankings.json"
    )

    with open(
        output_file,
        "w",
    ) as file:

        json.dump(
            rankings_json,
            file,
            indent=4,
        )


if __name__ == "__main__":

    build_rankings_json()