from EasyMode.RSI_PriceSolver.performance.annual_returns import (
    build_annual_returns,
)
def calculate_annual_table(
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