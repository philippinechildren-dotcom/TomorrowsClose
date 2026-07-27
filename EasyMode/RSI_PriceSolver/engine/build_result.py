from flask import request

from market_data.provider import get_market_history

from indicators.rsi_pricesolver import (
    solve_rsi_price,
)

from strategies.rsi_pricesolver_mean_reversion import (
    evaluate_rsi_pricesolver_mean_reversion,
)

from analytics.strategies.build_rsi_pricesolver import (
    build_rsi_pricesolver,
)

from analytics.strategies.build_buy_and_hold import (
    build_buy_and_hold,
)

from analytics.performance.metrics import (
    calculate_performance,
)

from catalog.strategies import get_strategy
from catalog.indicators import get_indicator

from pages.common import (
    add_common_page_data,
)


def build_result():

    strategy = get_strategy("rsi-pricesolver")
    indicator = get_indicator("rsi")

    ticker = request.args.get(
        "ticker",
        "QQQ",
    )

    defaults = strategy["default_parameters"][ticker]

    rsi_period = defaults["rsi_period"]

    threshold = defaults["threshold"]

    period = request.args.get(
        "period",
        "all",
    )

    history = get_market_history(
        ticker,
        bars=500,
    )

    solver_result = solve_rsi_price(
        closes=history["close"],
        period=rsi_period,
        target=threshold,
    )

    current_price = history["close"].iloc[-1]

    strategy_result = evaluate_rsi_pricesolver_mean_reversion(
        current_price=current_price,
        trigger_price=solver_result["exact_price"],
    )

    performance_result = build_rsi_pricesolver(
        ticker=ticker,
        rsi_length=rsi_period,
        threshold=threshold,
        period=period,
    )

    performance = calculate_performance(
        performance_result["equity_curve"],
        performance_result.get("closed_equity"),
    )

    result = {
        "ticker": ticker,
        "period": period,
        "rsi_period": rsi_period,
        "threshold": threshold,
        "current_price": round(
            float(current_price),
            2,
        ),
        "trigger_price": strategy_result["trigger_price"],
        "status": strategy_result["status"],
        "zone_title": strategy_result["zone_title"],
        "execution": strategy_result["execution"],
        "indicator": indicator,
        "performance": performance,
        "trade_metrics": performance_result["trade_metrics"],
        "annual_table": performance_result["annual_table"],
    }

    benchmark_result = build_buy_and_hold(
        ticker="QQQ",
        period=period,
    )

    benchmark_result["performance"] = calculate_performance(
        benchmark_result["equity_curve"],
    )

    result["benchmark"] = benchmark_result

    return add_common_page_data(
        result=result,
        strategy=strategy,
        history=history,
        indicator=indicator,
    )