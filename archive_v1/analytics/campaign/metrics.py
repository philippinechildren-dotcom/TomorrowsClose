from math import inf


def build_trade_metrics(
    records,
):
    """
    Calculate summary statistics from completed trades
    or completed campaigns.
    """

    if len(records) == 0:

        return {

            "count": 0,

            "win_rate": 0.0,

            "profit_factor": 0.0,

            "expectancy": 0.0,

            "kelly": 0.0,

            "average_bars": 0.0,

            "max_bars": 0,

            "max_consecutive_wins": 0,

            "max_consecutive_losses": 0,

        }

    count = len(records)

    winners = [
        r
        for r in records
        if r.winning_trade
    ]

    losers = [
        r
        for r in records
        if not r.winning_trade
    ]

    win_rate = (

        len(winners)

        /

        count

    )

    total_wins = sum(

        r.return_pct

        for r in winners

    )

    total_losses = sum(

        abs(r.return_pct)

        for r in losers

    )

    if total_losses > 0:

        profit_factor = (

            total_wins

            /

            total_losses

        )

    else:

        profit_factor = inf

    expectancy = (

        sum(

            r.return_pct

            for r in records

        )

        /

        count

    )

    average_bars = (

        sum(

            r.days_held

            for r in records

        )

        /

        count

    )

    max_bars = max(

        r.days_held

        for r in records

    )

    # ------------------------
    # Kelly %
    # ------------------------

    if (

        profit_factor != inf

        and profit_factor > 0

    ):

        kelly = (

            win_rate

            -

            (

                (1 - win_rate)

                /

                profit_factor

            )

        )

    else:

        kelly = 1.0

    # ------------------------
    # Consecutive wins/losses
    # ------------------------

    consecutive_wins = 0
    consecutive_losses = 0

    max_consecutive_wins = 0
    max_consecutive_losses = 0

    for record in records:

        if record.winning_trade:

            consecutive_wins += 1

            consecutive_losses = 0

            max_consecutive_wins = max(

                max_consecutive_wins,

                consecutive_wins,

            )

        else:

            consecutive_losses += 1

            consecutive_wins = 0

            max_consecutive_losses = max(

                max_consecutive_losses,

                consecutive_losses,

            )

    return {

        "count": count,

        "win_rate": win_rate,

        "profit_factor": profit_factor,

        "expectancy": expectancy,

        "kelly": kelly,

        "average_bars": average_bars,

        "max_bars": max_bars,

        "max_consecutive_wins": max_consecutive_wins,

        "max_consecutive_losses": max_consecutive_losses,

    }