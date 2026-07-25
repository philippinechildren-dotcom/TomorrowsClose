def calculate_trade_metrics(
    trades,
):
    """
    Calculate trade-based performance metrics.
    """

    if not trades:

        return {

            "trades": 0,

            "win_pct": None,

            "expectancy": None,

        }

    total = len(trades)

    winners = sum(
        1
        for trade in trades
        if trade.winning_trade
    )

    win_pct = winners / total

    expectancy = (

        sum(
            trade.return_pct
            for trade in trades
        )

        / total

    )

    return {

        "trades": total,

        "win_pct": win_pct,

        "expectancy": expectancy,

    }