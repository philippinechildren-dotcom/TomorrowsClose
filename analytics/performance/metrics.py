import math


def calculate_cagr(equity_curve):

    start = equity_curve[0]
    end = equity_curve[-1]

    years = len(equity_curve) / 252

    if years <= 0:
        return 0

    return (
        (end / start) ** (1 / years)
        - 1
    )


def calculate_max_eod_drawdown(equity_curve):

    peak = equity_curve[0]

    max_drawdown = 0

    for value in equity_curve:

        if value > peak:
            peak = value

        drawdown = (
            value / peak
            - 1
        )

        if drawdown < max_drawdown:
            max_drawdown = drawdown

    return max_drawdown


def calculate_max_closed_drawdown(
    closed_equity,
):

    if (
        closed_equity is None
        or
        len(closed_equity) < 2
    ):

        return None

    peak = closed_equity[0]

    max_drawdown = 0

    for value in closed_equity:

        if value > peak:

            peak = value

        drawdown = (

            value / peak

            - 1

        )

        if drawdown < max_drawdown:

            max_drawdown = drawdown

    return max_drawdown


def calculate_ulcer_index(equity_curve):

    peak = equity_curve[0]

    drawdowns = []

    for value in equity_curve:

        if value > peak:
            peak = value

        drawdown = (
            (value / peak)
            - 1
        ) * 100

        drawdowns.append(
            drawdown
        )

    squared = [
        value ** 2
        for value in drawdowns
    ]

    return math.sqrt(
        sum(squared)
        /
        len(squared)
    )


def calculate_upi(
    cagr,
    ulcer_index,
):

    if (
        ulcer_index is None
        or ulcer_index == 0
    ):

        return None

    return (

        cagr * 100

        /

        ulcer_index

    )


def calculate_performance(
    equity_curve,
    closed_equity=None,
):

    cagr = calculate_cagr(
        equity_curve
    )

    ulcer_index = calculate_ulcer_index(
        equity_curve
    )

    return {

        "period": "Rolling 1-Year",

        "cagr": cagr,

        "max_eod_drawdown": calculate_max_eod_drawdown(
            equity_curve
        ),

        "max_closed_drawdown": calculate_max_closed_drawdown(
            closed_equity
        ),

        "ulcer_index": ulcer_index,

        "upi": calculate_upi(
            cagr,
            ulcer_index,
        ),

    }