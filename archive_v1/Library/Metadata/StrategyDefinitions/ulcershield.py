STRATEGY_METADATA = {

    "type": "strategy",

    "name": "UlcerShield System",

    "slug": "ulcershield",

    "description":
        "A multi-layer RSI mean reversion system using five RSI PriceSolver signals.",

    "authors": [
        "william-michael-dejonge"
    ],

    "indicators": [
        "rsi"
    ],

    "category": "mean-reversion",

    "markets": [
        "etfs"
    ],

    "timeframe": "Daily",

    "difficulty": "Intermediate",

    "execution": "loc",

    "supports_pricesolver": True,

    "supports_intraday": False,

    "tags": [
        "pricesolver",
        "rsi",
        "mean-reversion"
    ],

    "default_parameters": {

        "ticker": "QQQ"

    },

    "rsi_systems": [

        {
            "name": "RSI1",
            "period": 2,
            "threshold": 30
        },

        {
            "name": "RSI2",
            "period": 3,
            "threshold": 30
        },

        {
            "name": "RSI3",
            "period": 5,
            "threshold": 30
        },

        {
            "name": "RSI4",
            "period": 8,
            "threshold": 30
        },

        {
            "name": "RSI5",
            "period": 13,
            "threshold": 34
        }

    ]

}