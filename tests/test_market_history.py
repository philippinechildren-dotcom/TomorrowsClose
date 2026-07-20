from market_data.provider import get_market_history


def main():
    history = get_market_history("QQQ", bars=500)

    print(history)

    print("\nNumber of bars:")
    print(len(history))

    print("\nLatest close:")
    print(history.iloc[-1]["close"])


if __name__ == "__main__":
    main()