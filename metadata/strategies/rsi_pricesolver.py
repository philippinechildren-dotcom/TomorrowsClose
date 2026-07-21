STRATEGY_METADATA = {
    "name": "RSI PriceSolver System",

    "slug": "rsi-pricesolver",

    "description": (
        "A mean reversion system using RSI PriceSolver "
        "to calculate the exact closing price required "
        "to trigger an entry or exit before the market close."
    ),

    "authors": [
        "William Michael DeJonge"
    ],

    "category": [
        "Mean Reversion"
    ],

    "markets": [
        "Stocks",
        "ETFs"
    ],

    "timeframe": "Daily",

    "difficulty": "Beginner",

    "tags": [
        "RSI",
        "Mean Reversion",
        "PriceSolver",
        "Limit-on-Close",
        "Daily Trading"
    ],

    "indicators": [
        "RSI"
    ],

    "related_strategies": [
        "rsi-threshold",
        "ulcershield"
    ],

    "related_indicators": [
        "rsi"
    ],

    "execution": "Limit-on-Close",

    "template": "pricesolver",

    "strategy_module": "rsi_pricesolver_mean_reversion"
}