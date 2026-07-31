from analytics.strategies.build_buy_and_hold import (
    build_buy_and_hold,
)

from analytics.strategies.performance import (
    build_performance_report,
)

result = build_buy_and_hold(
    ticker="QQQ",
    period="all",
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
print("Buy & Hold Performance")
print("----------------------")

for key, value in report.items():

    if key != "equity_curve":

        print(f"{key}: {value}")

print()
print("Trade Metrics")
print("-------------")
print(result["trade_metrics"])

print()
print("Annual Table")
print("------------")

for row in result["annual_table"]:

    print(row)