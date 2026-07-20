from market_data.provider import get_market_history
from indicators.rsi_pricesolver import solve_rsi_price


def main():

    history = get_market_history("QQQ", bars=500)

    result = solve_rsi_price(
        history["close"],
        period=3,
        target=30
    )

    print("Current close:")
    print(history.iloc[-1]["close"])

    print("\nCurrent RSI:")
    print(round(result["current_rsi"], 4))

    print("\nTarget RSI:")
    print(result["target_rsi"])

    print("\nExact Price:")
    print(result["exact_price"])


if __name__ == "__main__":
    main()