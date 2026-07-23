from analytics.strategies.build_rsi_pricesolver import (
    build_rsi_pricesolver,
)

from analytics.strategies.performance import (
    build_performance_report,
)


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


print()

print("RSI PriceSolver Performance")

print("---------------------------")

for key, value in report.items():

    if key != "equity_curve":

        print(f"{key}: {value}")