from Other_Strategies.Trend_Following.Buy_and_Hold.performance.build_strategy import (
    build_buy_and_hold,
)
from EasyMode.LowHigh.performance.build_strategy import build_lowhigh
from EasyMode.RSI_PriceSolver.performance.performance_pipeline import (
    build_rsi_pricesolver,
)
from EasyMode.UlcerShield.performance.build_strategy import build_ulcershield


BUILDERS = {
    "buy-and-hold": build_buy_and_hold,
    "lowhigh": build_lowhigh,
    "rsi-pricesolver": build_rsi_pricesolver,
    "ulcershield": build_ulcershield,
}


def build_annual_performance(strategy):

    if strategy not in BUILDERS:
        raise ValueError(f"Unknown strategy: {strategy}")

    result = BUILDERS[strategy]()

    return {
        "strategy": strategy,
        "ticker": result["ticker"],
        "annual_table": result["annual_table"],
    }