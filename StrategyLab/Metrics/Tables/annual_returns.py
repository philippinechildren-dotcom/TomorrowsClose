"""
StrategyLab/Metrics/Tables/annual_returns.py
"""


def build_annual_returns(
    strategy_result,
):
    """
    Build Annual Returns table.
    """

    # ==========================================================
    # Annual Returns Accounting Convention
    # ==========================================================
    #
    # Trades belong entirely to the calendar year in which
    # they CLOSE.
    #
    # Open trades are never marked-to-market at year end.
    #
    # Annual Return and Max EOD DD are calculated only from
    # campaigns closing during that year.
    # ==========================================================

    trades = sorted(
        strategy_result["trades"],
        key=lambda trade: trade.exit_date,
    )

    if not trades:
        return []

    annual_returns = []

    current_year = None

    starting_equity = strategy_result["starting_equity"]

    equity = starting_equity

    peak_equity = starting_equity

    max_eod_drawdown = 0.0

    for trade in trades:

        exit_year = trade.exit_date.year

        if current_year is None:

            current_year = exit_year

        elif exit_year != current_year:

            ending_equity = equity

            annual_return = (
                ending_equity
                / starting_equity
            ) - 1.0

            annual_returns.append(
                {
                    "year": current_year,
                    "return": annual_return,
                    "max_eod_drawdown": max_eod_drawdown,
                }
            )

            current_year = exit_year

            starting_equity = equity

            peak_equity = equity

            max_eod_drawdown = 0.0

        equity += trade.pnl

        if equity > peak_equity:
            peak_equity = equity

        drawdown = (
            equity
            - peak_equity
        ) / peak_equity

        if drawdown < max_eod_drawdown:
            max_eod_drawdown = drawdown

    ending_equity = equity

    annual_return = (
        ending_equity
        / starting_equity
    ) - 1.0

    annual_returns.append(
        {
            "year": current_year,
            "return": annual_return,
            "max_eod_drawdown": max_eod_drawdown,
        }
    )

    annual_returns.sort(
        key=lambda row: row["year"],
        reverse=True,
    )

    return annual_returns