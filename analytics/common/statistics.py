from math import pow


def calculate_total_return(
    starting_equity: float,
    ending_equity: float,
) -> float:
    """
    Total return as a decimal.

    Example:
        0.25 = 25%
    """

    if starting_equity <= 0:
        return 0.0

    return (
        ending_equity / starting_equity
    ) - 1


def calculate_cagr(
    starting_equity: float,
    ending_equity: float,
    years: float,
) -> float:
    """
    CAGR returned as a decimal.

    Example:
        0.27 = 27%
    """

    if (
        years <= 0
        or starting_equity <= 0
    ):
        return 0.0

    return (
        pow(
            ending_equity / starting_equity,
            1 / years
        )
        - 1
    )


def calculate_win_rate(
    wins: int,
    total_trades: int,
) -> float:
    """
    Win rate returned as a decimal.

    Example:
        0.82 = 82%
    """

    if total_trades == 0:
        return 0.0

    return wins / total_trades


def calculate_profit_factor(
    gross_profit: float,
    gross_loss: float,
) -> float:
    """
    Profit Factor.

    Gross loss should be positive.
    """

    if gross_loss <= 0:
        return 0.0

    return gross_profit / gross_loss


def calculate_expectancy(
    net_profit: float,
    total_trades: int,
) -> float:
    """
    Average profit per trade.
    """

    if total_trades == 0:
        return 0.0

    return net_profit / total_trades


def calculate_time_in_market(
    bars_in_market: int,
    total_bars: int,
) -> float:
    """
    Time in market returned as a decimal.

    Example:
        0.34 = 34%
    """

    if total_bars == 0:
        return 0.0

    return bars_in_market / total_bars