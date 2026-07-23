from analytics.common.drawdown import (
    calculate_equity_drawdowns,
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
) -> dict:
    """
    Build standardized strategy performance report.

    Used by all strategy analytics.

    Calculates:
    - total return
    - CAGR
    - max EOD drawdown
    - Ulcer Index
    - UPI
    - trade statistics
    """

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

        "ulcer_index": ulcer_index,

        "upi": upi,

        "trade_metrics": trade_metrics,

        "equity_curve": equity_curve,

        "years": years,

    }