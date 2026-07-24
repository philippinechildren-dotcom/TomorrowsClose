from analytics.strategies.build_ulcershield import (
    build_ulcershield,
)

from analytics.strategies.performance import (
    build_performance_report,
)


result = build_ulcershield(
    ticker="TQQQ",
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
print("UlcerShield Performance")
print("-----------------------")

for key, value in report.items():

    if key != "equity_curve":

        print(f"{key}: {value}")


print()
print("Summary")
print("-------")
print(f"Signals: {len(result['signals'])}")
print(f"Trades: {len(result['trades'])}")

if "campaigns" in result:
    print(f"Campaigns: {len(result['campaigns'])}")