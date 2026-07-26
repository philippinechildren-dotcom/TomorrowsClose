from market_data.provider import get_market_history

history = get_market_history("TQQQ")

history = history[
    history.index.year == 2012
]

print(history[["close"]].to_string())