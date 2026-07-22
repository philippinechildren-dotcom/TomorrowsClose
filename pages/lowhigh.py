from flask import request

from market_data.provider import get_market_history

from strategies.lowhigh import (
    calculate_lowhigh,
)

from catalog.strategies import get_strategy

from pages.common import (
    add_common_page_data,
)


def build_result():

    strategy = get_strategy("lowhigh")

    defaults = strategy["default_parameters"]

    ticker = request.args.get(
        "ticker",
        defaults["ticker"]
    )

    entry_lookback = int(
        request.args.get(
            "entry_lookback",
            defaults["entry_lookback"]
        )
    )

    exit_lookback = int(
        request.args.get(
            "exit_lookback",
            defaults["exit_lookback"]
        )
    )

    history = get_market_history(
        ticker,
        bars=500
    )

    result = calculate_lowhigh(
        ticker=ticker,
        history=history,
        entry_lookback=entry_lookback,
        exit_lookback=exit_lookback,
    )

    return add_common_page_data(
        result=result,
        strategy=strategy,
        history=history,
    )