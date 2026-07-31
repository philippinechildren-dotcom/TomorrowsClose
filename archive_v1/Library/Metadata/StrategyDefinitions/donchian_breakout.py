STRATEGY_METADATA = {

    "type": "strategy",

    "name": "Donchian Breakout",

    "slug": "donchian-breakout",

    "description":
        "A long-only trend following strategy that buys when price crosses above a long-term Donchian high and exits when price crosses below a long-term Donchian low using stop orders.",

    "authors": [
        "Richard Donchian"
    ],

    "indicators": [
        "donchian"
    ],

    "category": "trend-following",

    "markets": [
        "etfs",
        "stocks"
    ],

    "timeframe": "Daily",

    "difficulty": "Beginner",

    "execution": "stop",

    "supports_pricesolver": True,

    "supports_intraday": False,

    "signal_structure": "two_zone_trend",

    "tags": [
        "donchian",
        "breakout",
        "trend-following",
        "momentum",
        "pricesolver"
    ],

    "default_parameters": {

        "ticker": "QQQ",

        "entry_lookback": 100,

        "exit_lookback": 250,

        "entry_source": "highest_close",

        "exit_source": "lowest_close",

    }

}