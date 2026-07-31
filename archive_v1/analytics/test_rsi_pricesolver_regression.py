from analytics.strategies.build_rsi_pricesolver import (
    build_rsi_pricesolver,
)


def run_test():

    result = build_rsi_pricesolver(
        ticker="TQQQ",
        rsi_length=3,
        threshold=28,
    )


    assert result["starting_equity"] == 100000.0, (
        "Starting equity changed"
    )


    assert len(result["trades"]) > 0, (
        "No trades generated"
    )


    report = result


    ending_equity = report["ending_equity"]

    total_return = (
        ending_equity /
        report["starting_equity"]
        - 1
    )


    assert total_return > 0.20, (
        "Return unexpectedly low"
    )


    print("RSI PriceSolver regression test passed")

    print("----------------------------------")

    print(
        f"Trades: {len(result['trades'])}"
    )

    print(
        f"Ending Equity: {ending_equity:,.2f}"
    )

    print(
        f"Return: {total_return:.2%}"
    )



if __name__ == "__main__":

    run_test()