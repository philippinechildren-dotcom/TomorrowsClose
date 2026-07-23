from analytics.strategies.build_lowhigh import (
    build_lowhigh,
)



def run_test():

    result = build_lowhigh(
        ticker="QLD",
        lookback=3,
    )


    assert result["starting_equity"] == 100000.0, (
        "Starting equity changed"
    )


    assert len(result["trades"]) > 0, (
        "No trades generated"
    )


    total_return = (

        result["ending_equity"]

        /

        result["starting_equity"]

        - 1

    )


    assert total_return > 0, (
        "Strategy is no longer profitable"
    )


    assert len(result["trades"]) >= 5, (
        "Unexpectedly low trade count"
    )


    print()

    print("LowHigh regression test passed")

    print("----------------------------")


    print(
        f"Trades: {len(result['trades'])}"
    )

    print(
        f"Ending Equity: {result['ending_equity']:,.2f}"
    )

    print(
        f"Return: {total_return:.2%}"
    )

    print(
        f"Lookback: {result['lookback']}"
    )



if __name__ == "__main__":

    run_test()