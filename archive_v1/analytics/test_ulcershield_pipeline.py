from EasyMode.UlcerShield.performance.build_strategy import (
    build_ulcershield,
)

from analytics.strategies.performance import (
    build_performance_report,
)

result = build_ulcershield(
    ticker="TQQQ",
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
print("UlcerShield Performance")
print("-----------------------")

for key, value in report.items():

    if key != "equity_curve":

        print(f"{key}: {value}")

print()
print("Campaign Metrics")
print("----------------")
print(result["campaign_metrics"])

print()
print("Parameters")
print("----------")
print(f"Ticker: {result['ticker']}")
print(f"RSI Lengths: {result['rsi_lengths']}")
print(f"Thresholds: {result['thresholds']}")

print()
print("Annual Table")
print("------------")

for row in result["annual_table"]:

    print(row)