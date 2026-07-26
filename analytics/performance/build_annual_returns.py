from collections import defaultdict


def build_annual_returns(
    trades,
    equity_curve,
    equity_dates,
):
    """
    Build calendar-year compounded returns
    and calendar-year Max EOD drawdowns.
    """

    yearly_equity = defaultdict(list)

    for date, equity in zip(
        equity_dates,
        equity_curve,
    ):
        yearly_equity[date.year].append(equity)

    yearly_returns = {}

    for year, values in yearly_equity.items():
        if len(values) >= 2:
            yearly_returns[year] = (
                values[-1] / values[0] - 1
            ) * 100
        else:
            yearly_returns[year] = 0.0

    yearly_drawdowns = {}

    current_year = None
    peak = None
    max_dd = 0.0

    for date, equity in zip(
        equity_dates,
        equity_curve,
    ):
        year = date.year

        if current_year != year:
            if current_year is not None:
                yearly_drawdowns[current_year] = max_dd * 100

            current_year = year
            peak = equity
            max_dd = 0.0

        if equity > peak:
            peak = equity

        drawdown = equity / peak - 1

        if drawdown < max_dd:
            max_dd = drawdown

    if current_year is not None:
        yearly_drawdowns[current_year] = max_dd * 100

    years = sorted(
        set(yearly_returns)
        | set(yearly_drawdowns),
        reverse=True,
    )

    annual_results = []

    for year in years:
        ret = yearly_returns.get(
            year,
            0.0,
        )

        annual_results.append({
            "year": year,
            "return_pct": ret,
            "max_eod_dd": yearly_drawdowns.get(
                year,
                0.0,
            ),
            "positive": ret >= 0,
        })

    return annual_results