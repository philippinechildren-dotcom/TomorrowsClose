from collections import defaultdict


def build_annual_returns(
    trades,
    equity_curve,
    equity_dates,
):
    """
    Build yearly compounded returns and
    calendar-year Max EOD drawdowns.
    """

    # -----------------------------
    # YEARLY COMPOUNDED RETURNS
    # -----------------------------

    yearly_growth = defaultdict(
        lambda: 1.0
    )

    for trade in trades:

        year = trade.exit_date.year

        yearly_growth[year] *= (
            1 + trade.return_pct
        )

    yearly_returns = {}

    for year, growth in yearly_growth.items():

        yearly_returns[year] = (
            growth - 1
        ) * 100

    # -----------------------------
    # YEARLY MAX EOD DRAWDOWN
    # -----------------------------

    yearly_drawdowns = {}

    current_year = None

    peak = None

    max_dd = 0.0

    for date, equity in zip(
        equity_dates,
        equity_curve,
    ):

        year = date.year

        if current_year is None:

            current_year = year

            peak = equity

            max_dd = 0.0

        elif year != current_year:

            yearly_drawdowns[
                current_year
            ] = max_dd * 100

            current_year = year

            peak = equity

            max_dd = 0.0

        if equity > peak:

            peak = equity

        drawdown = (
            equity / peak
            - 1
        )

        if drawdown < max_dd:

            max_dd = drawdown

    # Save final year's drawdown

    if current_year is not None:

        yearly_drawdowns[
            current_year
        ] = max_dd * 100

    # -----------------------------
    # BUILD FINAL TABLE
    # -----------------------------

    all_years = sorted(

        set(yearly_returns.keys())

        |

        set(yearly_drawdowns.keys()),

        reverse=True,

    )

    annual_results = []

    for year in all_years:

        return_pct = yearly_returns.get(
            year,
            0.0,
        )

        max_eod_dd = yearly_drawdowns.get(
            year,
            0.0,
        )

        annual_results.append({

            "year": year,

            "return_pct": return_pct,

            "max_eod_dd": max_eod_dd,

            "positive": return_pct >= 0,

        })

    return annual_results