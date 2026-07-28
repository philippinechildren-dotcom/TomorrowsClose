from market_data.provider import get_market_history
from indicators.rsi_pricesolver import (
    solve_rsi_price,
)
from EasyMode.RSI_PriceSolver.logic.signal_logic import (
    evaluate_rsi_pricesolver_mean_reversion,
)

def calculate_signal(
    ticker,
    rsi_period,
    threshold,
):

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

    return {
        "history": history,
        "current_price": round(
            float(current_price),
            2,
        ),
        "trigger_price": strategy_result["trigger_price"],
        "status": strategy_result["status"],
        "zone_title": strategy_result["zone_title"],
        "execution": strategy_result["execution"],
    }