from flask import render_template

from StrategyLab.Benchmarks.buy_and_hold import build_result as build_buy_and_hold_result
from StrategyLab.Strategies.lowhigh import build_result as build_lowhigh_result
from StrategyLab.Strategies.rsi_threshold import build_result as build_rsi_threshold_result
from StrategyLab.Strategies.ulcershield import build_result as build_ulcershield_result

from Rankings.rankings import build_rankings


def build_result():

    buy_and_hold = build_buy_and_hold_result()
    lowhigh = build_lowhigh_result()
    rsi_threshold = build_rsi_threshold_result()
    ulcershield = build_ulcershield_result()

    return build_rankings(
        [
            buy_and_hold,
            lowhigh,
            rsi_threshold,
            ulcershield,
        ],
        rank_by="ulcer_performance_index",
    )


def render_page():

    return render_template(
        "display_components/rankings/rankings.html",
        rankings=build_result(),
    )