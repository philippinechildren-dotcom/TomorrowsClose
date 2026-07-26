from analytics.strategies.build_buy_and_hold import build_buy_and_hold
from analytics.strategies.build_lowhigh import build_lowhigh
from analytics.strategies.build_rsi_pricesolver import build_rsi_pricesolver
from analytics.strategies.build_ulcershield import build_ulcershield


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