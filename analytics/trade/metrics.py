def calculate_trade_metrics(
    trades: list,
) -> dict:
    """
    Calculate statistics from completed trades.

    Expects a list of Trade objects from
    analytics.trade.engine
    """

    if not trades:

        return {

            "trade_count": 0,

            "win_rate": 0,

            "profit_factor": 0,

            "expectancy": 0,

            "average_win": 0,

            "average_loss": 0,

            "max_consecutive_wins": 0,

            "max_consecutive_losses": 0,

        }


    winners = [

        trade.pnl

        for trade in trades

        if trade.pnl > 0

    ]


    losers = [

        trade.pnl

        for trade in trades

        if trade.pnl <= 0

    ]


    total_profit = sum(winners)

    total_loss = abs(sum(losers))


    profit_factor = (

        total_profit / total_loss

        if total_loss > 0

        else float("inf")

    )


    average_win = (

        sum(winners) / len(winners)

        if winners

        else 0

    )


    average_loss = (

        sum(losers) / len(losers)

        if losers

        else 0

    )


    expectancy = (

        sum(trade.pnl for trade in trades)

        /

        len(trades)

    )


    consecutive_wins = 0

    consecutive_losses = 0

    max_consecutive_wins = 0

    max_consecutive_losses = 0


    for trade in trades:

        if trade.pnl > 0:

            consecutive_wins += 1

            consecutive_losses = 0

        else:

            consecutive_losses += 1

            consecutive_wins = 0


        max_consecutive_wins = max(

            max_consecutive_wins,

            consecutive_wins

        )


        max_consecutive_losses = max(

            max_consecutive_losses,

            consecutive_losses

        )


    return {

        "trade_count": len(trades),

        "win_rate": (

            len(winners)

            /

            len(trades)

        ),

        "profit_factor": profit_factor,

        "expectancy": expectancy,

        "average_win": average_win,

        "average_loss": average_loss,

        "max_consecutive_wins": max_consecutive_wins,

        "max_consecutive_losses": max_consecutive_losses,

    }