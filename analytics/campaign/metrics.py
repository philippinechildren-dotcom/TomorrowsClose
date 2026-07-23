from math import inf


def build_campaign_metrics(
    campaigns,
):
    """
    Calculate summary statistics from completed campaigns.
    """

    if len(campaigns) == 0:

        return {

            "campaign_count": 0,

            "campaign_win_rate": 0.0,

            "campaign_profit_factor": 0.0,

            "campaign_expectancy": 0.0,

            "campaign_kelly": 0.0,

            "average_campaign_bars": 0.0,

            "max_campaign_bars": 0,

            "max_consecutive_wins": 0,

            "max_consecutive_losses": 0,

        }


    campaign_count = len(campaigns)


    winners = [
        c
        for c in campaigns
        if c.winning_campaign
    ]


    losers = [
        c
        for c in campaigns
        if not c.winning_campaign
    ]


    campaign_win_rate = (

        len(winners)

        /

        campaign_count

    )


    total_wins = sum(

        c.return_pct

        for c in winners

    )


    total_losses = sum(

        abs(c.return_pct)

        for c in losers

    )


    if total_losses > 0:

        campaign_profit_factor = (

            total_wins

            /

            total_losses

        )

    else:

        campaign_profit_factor = inf


    campaign_expectancy = (

        sum(

            c.return_pct

            for c in campaigns

        )

        /

        campaign_count

    )


    average_campaign_bars = (

        sum(

            c.bars_held

            for c in campaigns

        )

        /

        campaign_count

    )


    max_campaign_bars = max(

        c.bars_held

        for c in campaigns

    )


    # ------------------------
    # Kelly %
    # ------------------------

    if (

        campaign_profit_factor != inf

        and campaign_profit_factor > 0

    ):

        campaign_kelly = (

            campaign_win_rate

            -

            (

                (1 - campaign_win_rate)

                /

                campaign_profit_factor

            )

        )

    else:

        campaign_kelly = 1.0


    # ------------------------
    # Consecutive wins/losses
    # ------------------------

    consecutive_wins = 0
    consecutive_losses = 0

    max_consecutive_wins = 0
    max_consecutive_losses = 0


    for campaign in campaigns:

        if campaign.winning_campaign:

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

        "campaign_count": campaign_count,

        "campaign_win_rate": campaign_win_rate,

        "campaign_profit_factor": campaign_profit_factor,

        "campaign_expectancy": campaign_expectancy,

        "campaign_kelly": campaign_kelly,

        "average_campaign_bars": average_campaign_bars,

        "max_campaign_bars": max_campaign_bars,

        "max_consecutive_wins": max_consecutive_wins,

        "max_consecutive_losses": max_consecutive_losses,

    }