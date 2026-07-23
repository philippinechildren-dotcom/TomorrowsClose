def calculate_equity_drawdowns(equity_curve: list[float]) -> dict:
    """
    Calculate maximum end-of-day drawdown from an equity curve.

    Parameters
    ----------
    equity_curve : list[float]
        Sequential equity values.

    Returns
    -------
    dict

        {
            "max_drawdown": float,
            "drawdowns": list[float],
        }
    """

    if not equity_curve:
        return {
            "max_drawdown": 0.0,
            "drawdowns": [],
        }

    peak = equity_curve[0]

    drawdowns = []

    max_drawdown = 0.0

    for equity in equity_curve:

        if equity > peak:
            peak = equity

        dd = (peak - equity) / peak

        drawdowns.append(dd)

        if dd > max_drawdown:
            max_drawdown = dd

    return {

        "max_drawdown": max_drawdown,

        "drawdowns": drawdowns,

    }


def calculate_closed_drawdown(closed_equity: list[float]) -> float:
    """
    Calculate maximum closed-position drawdown.

    Parameters
    ----------
    closed_equity : list[float]

        Equity after each completed trade or campaign.

    Returns
    -------
    float
    """

    if not closed_equity:
        return 0.0

    peak = closed_equity[0]

    max_drawdown = 0.0

    for equity in closed_equity:

        if equity > peak:
            peak = equity

        dd = (peak - equity) / peak

        if dd > max_drawdown:
            max_drawdown = dd

    return max_drawdown