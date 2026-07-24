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


def calculate_performance(equity_curve):

    return {

        "period": "Rolling 1-Year",

        "cagr": calculate_cagr(
            equity_curve
        ),

        "max_eod_drawdown": calculate_max_eod_drawdown(
            equity_curve
        ),

        "ulcer_index": calculate_ulcer_index(
            equity_curve
        ),

    }