"""
StrategyLab/Metrics/Tables/annual_returns.py
"""


def build_annual_returns(
    strategy_result,
):
    """
    Build Annual Returns table.

    Reporting convention:

    - Performance is based on completed trades.
    - A trade belongs to the calendar year in which it closes.
    - A trade that began before the year is included when it closes
      during the year.
    - A trade still open at year end is excluded until it closes.
    """

    trades = sorted(
        strategy_result["trades"],
        key=lambda trade: trade.exit_date,
    )

    if not trades:
        return []

    annual_returns = []

    starting_equity = strategy_result["starting_equity"]
    equity = starting_equity

    current_year = None
    year_starting_equity = None
    year_peak_equity = None
    year_max_drawdown = 0.0

    for trade in trades:

        exit_year = trade.exit_date.year

        if current_year is None:

            current_year = exit_year
            year_starting_equity = equity
            year_peak_equity = equity
            year_max_drawdown = 0.0

        elif exit_year != current_year:

            annual_return = (
                equity
                / year_starting_equity
            ) - 1.0

            annual_returns.append(
                {
                    "year": current_year,
                    "return": annual_return,
                    "max_eod_drawdown": year_max_drawdown,
                }
            )

            current_year = exit_year
            year_starting_equity = equity
            year_peak_equity = equity
            year_max_drawdown = 0.0

        equity += trade.pnl

        if equity > year_peak_equity:
            year_peak_equity = equity

        drawdown = (
            equity - year_peak_equity
        ) / year_peak_equity

        if drawdown < year_max_drawdown:
            year_max_drawdown = drawdown

    annual_return = (
        equity
        / year_starting_equity
    ) - 1.0

    annual_returns.append(
        {
            "year": current_year,
            "return": annual_return,
            "max_eod_drawdown": year_max_drawdown,
        }
    )

    annual_returns.sort(
        key=lambda row: row["year"],
        reverse=True,
    )

    return annual_returns