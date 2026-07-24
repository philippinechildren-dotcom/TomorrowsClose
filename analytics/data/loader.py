import json
from pathlib import Path


CACHE_FILE = (
    Path(__file__).parent
    / "performance_cache.json"
)


def load_cache():

    with open(CACHE_FILE, "r") as f:
        return json.load(f)


def get_strategies():

    return load_cache()["strategies"]


def get_strategy(
    strategy,
    ticker,
):

    for item in get_strategies():

        if (
            item["strategy"] == strategy
            and item["ticker"] == ticker
        ):
            return item

    return None