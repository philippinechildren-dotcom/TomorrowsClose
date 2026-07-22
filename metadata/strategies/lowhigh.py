STRATEGY_METADATA = {

    "type": "strategy",

    "name": "LowHigh System",

    "slug": "lowhigh",

    "description":
        "A mean reversion strategy that buys below the previous Donchian low and exits above the previous Donchian high using Limit-on-Close orders.",

    "authors": [
        "william-michael-dejonge"
    ],

    "indicators": [
        "donchian"
    ],

    "category": "mean-reversion",

    "markets": [
        "etfs"
    ],

    "timeframe": "Daily",

    "difficulty": "Beginner",

    "execution": "loc",

    "supports_pricesolver": True,

    "supports_intraday": False,

    "tags": [
        "donchian",
        "mean-reversion",
        "pricesolver"
    ],

    "default_parameters": {

        "ticker": "QLD",

        "entry_lookback": 3,

        "exit_lookback": 1,

    }

}