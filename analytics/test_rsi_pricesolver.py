from analytics.strategies.build_rsi_pricesolver import (
    build_rsi_pricesolver,
)

from analytics.strategies.performance import (
    build_performance_report,
)


def run_test():

    result = build_rsi_pricesolver(
        ticker="TQQQ",
        rsi_length=3,
        threshold=28,
    )

    report = build_performance_report(
        starting_equity=result["starting_equity"],
        ending_equity=result["ending_equity"],
        equity_curve=result["equity_curve"],
        start_date=result["start_date"],
        end_date=result["end_date"],
        trades=result["trades"],
    )

    print(result["equity_dates"][0])
    print(result["equity_dates"][-1])

    print()
    print("RSI PriceSolver Performance")
    print("---------------------------")

    for key, value in report.items():
        if key != "equity_curve":
            print(f"{key}: {value}")

    print()
    print("Parameters")
    print("----------")
    print(f"Ticker: {result['ticker']}")
    print(f"RSI Length: {result['rsi_length']}")
    print(f"Threshold: {result['threshold']}")

    print()
    print("First 10 Trades")
    print("---------------")

    for trade in result["trades"][:10]:
        print(
            trade.entry_date,
            trade.exit_date,
            round(trade.entry_price, 2),
            round(trade.exit_price, 2),
            round(trade.return_pct * 100, 2),
        )

    print()
    print("Annual Table")
    print("------------")

    for row in result["annual_table"]:
        print(row)


if __name__ == "__main__":
    run_test()