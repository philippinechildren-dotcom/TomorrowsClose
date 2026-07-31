import math


def calculate_ulcer_index(drawdowns: list[float]) -> float:
    """
    Calculate the Ulcer Index from a list of drawdowns.

    Parameters
    ----------
    drawdowns : list[float]

        Drawdowns expressed as decimals.

        Example:
            0.10 = 10% drawdown

    Returns
    -------
    float
    """

    if not drawdowns:
        return 0.0

    squared_sum = 0.0

    for dd in drawdowns:
        squared_sum += (dd * 100) ** 2

    return math.sqrt(
        squared_sum / len(drawdowns)
    )


def calculate_upi(
    cagr: float,
    ulcer_index: float,
) -> float:
    """
    Calculate the Ulcer Performance Index.

    Parameters
    ----------
    cagr : float

        Annualized return expressed as a decimal.

        Example:
            0.27 = 27%

    ulcer_index : float

        Ulcer Index expressed in percentage points.

        Example:
            2.74

    Returns
    -------
    float
    """

    if ulcer_index <= 0:
        return 0.0

    return (cagr * 100) / ulcer_index