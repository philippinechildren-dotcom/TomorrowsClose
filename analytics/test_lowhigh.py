from analytics.strategies.build_lowhigh import (
    build_lowhigh,
)

from analytics.strategies.performance import (
    build_performance_report,
)



def run_test():

    result = build_lowhigh(
        ticker="QLD",
        lookback=3,
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

    print("LowHigh Performance")

    print("-------------------")


    for key, value in report.items():

        if key != "equity_curve":

            print(
                f"{key}: {value}"
            )



    print()

    print("Parameters")

    print("----------")

    print(
        f"Ticker: {result['ticker']}"
    )

    print(
        f"Lookback: {result['lookback']}"
    )



if __name__ == "__main__":

    run_test()