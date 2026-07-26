# TODO:
# This page should display ALL-TIME performance metrics.
# It currently calls the strategy page builders, which default to the
# strategy page period (currently 1 Year). During the performance refactor,
# modify the strategy page builders to accept a period parameter
# (e.g. build_result(period="all")) so this page can request lifetime metrics
# without affecting the strategy pages.

import json
from pathlib import Path

CACHE_DIR = Path("analytics/data/cache")

from pages.lowhigh import build_result as build_lowhigh_result
from pages.rsi_pricesolver import build_result as build_rsi_pricesolver_result
from pages.ulcershield import build_result as build_ulcershield_result


def build_performance_summary_vertical(strategy, period="all"):

    if strategy == "lowhigh":
        result = build_lowhigh_result()

    elif strategy == "rsi-pricesolver":
        result = build_rsi_pricesolver_result()

    elif strategy == "ulcershield":
        result = build_ulcershield_result()

    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    with open(CACHE_DIR / "buy_and_hold_qqq.json") as f:
        result["benchmark"] = json.load(f)

    return result