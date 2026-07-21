STRATEGY_METADATA = {

    "type": "strategy",

    "name": "RSI PriceSolver System",

    "slug": "rsi-pricesolver",

    "description":
        "A mean reversion strategy that reverse-calculates the closing price required to produce an RSI buy or sell signal before the market closes.",

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

    "difficulty": "Beginner",

    "execution": "loc",

    "supports_pricesolver": True,

    "supports_intraday": False,

    "tags": [
        "pricesolver"
    ],

    "default_parameters": {

        "ticker": "QQQ",

        "rsi_period": 3,

        "threshold": 30

    }

}