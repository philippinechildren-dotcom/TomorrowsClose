from market_data.provider import get_market_history
from indicators.rsi_calculator import calculate_rsi


def main():
    history = get_market_history("QQQ", bars=500)

    rsi = calculate_rsi(
        history["close"],
        period=3
    )

    print("Latest close:")
    print(history.iloc[-1]["close"])

    print("\nLatest RSI(3):")
    print(round(rsi.iloc[-1], 2))


if __name__ == "__main__":
    main()