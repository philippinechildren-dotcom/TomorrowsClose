from analytics.performance.build_annual_returns import build_annual_returns


def build_annual_table(
    trades,
    equity_curve,
    equity_dates,
):
    rows = build_annual_returns(
        trades=trades,
        equity_curve=equity_curve,
        equity_dates=equity_dates,
    )

    rows.sort(
        key=lambda x: x["year"],
        reverse=True,
    )

    return rows