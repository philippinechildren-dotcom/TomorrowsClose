from analytics.strategies.build_buy_and_hold import (
    build_buy_and_hold,
)

from analytics.strategies.performance import (
    build_performance_report,
)


result = build_buy_and_hold(
    "QQQ"
)


report = build_performance_report(

    starting_equity=result["starting_equity"],

    ending_equity=result["ending_equity"],

    equity_curve=result["equity_curve"],

    start_date=result["start_date"],
    end_date=result["end_date"],

)


print()

for key, value in report.items():

    if key != "equity_curve":

        print(f"{key}: {value}")