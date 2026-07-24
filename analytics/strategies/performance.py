from analytics.common.drawdown import (
    calculate_equity_drawdowns,
    calculate_closed_drawdown,
)

from analytics.common.ulcer import (
    calculate_ulcer_index,
    calculate_upi,
)

from analytics.common.statistics import (
    calculate_total_return,
    calculate_cagr,
)

from analytics.trade.metrics import (
    calculate_trade_metrics,
)


def build_performance_report(
    starting_equity: float,
    ending_equity: float,
    equity_curve: list,
    start_date,
    end_date,
    trades: list | None = None,
    campaigns: list | None = None,
) -> dict:

    years = (
        end_date - start_date
    ).days / 365.25

    total_return = calculate_total_return(
        starting_equity,
        ending_equity,
    )

    cagr = calculate_cagr(
        starting_equity,
        ending_equity,
        years,
    )

    drawdown = calculate_equity_drawdowns(
        equity_curve,
    )

    ulcer_index = calculate_ulcer_index(
        drawdown["drawdowns"],
    )

    upi = calculate_upi(
        cagr,
        ulcer_index,
    )

    closed_drawdown = 0.0

    if trades:

        closed_equity = [starting_equity]

        equity = starting_equity

        for trade in trades:

            equity += trade.pnl

            closed_equity.append(equity)

        closed_drawdown = calculate_closed_drawdown(
            closed_equity
        )

    trade_metrics = (
        calculate_trade_metrics(trades)
        if trades is not None
        else {}
    )

    return {
        "starting_equity": starting_equity,
        "ending_equity": ending_equity,
        "total_return": total_return,
        "cagr": cagr,
        "max_eod_drawdown": drawdown["max_drawdown"],
        "max_closed_drawdown": closed_drawdown,
        "ulcer_index": ulcer_index,
        "upi": upi,
        "trade_metrics": trade_metrics,
        "equity_curve": equity_curve,
        "years": years,
    }