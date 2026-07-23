from dataclasses import dataclass


@dataclass
class Campaign:
    """
    One completed investment campaign.

    A campaign begins when the portfolio goes from
    completely flat to having at least one active
    position.

    A campaign ends when the final open position
    is closed.
    """

    start_date: object
    end_date: object

    start_equity: float
    end_equity: float

    return_pct: float

    bars_held: int

    winning_campaign: bool



def build_campaigns(
    daily_states,
):
    """
    Build completed campaigns.

    Parameters
    ----------
    daily_states : list

        Each element should contain:

        {
            "date": ...,
            "portfolio_active": bool,
            "closed_equity": float,
        }

    Returns
    -------
    list[Campaign]
    """

    campaigns = []

    active = False

    start_date = None
    start_equity = None

    bars = 0


    for day in daily_states:

        date = day["date"]

        portfolio_active = day["portfolio_active"]

        closed_equity = float(
            day["closed_equity"]
        )


        # --------------------------
        # Campaign begins
        # --------------------------

        if portfolio_active and not active:

            active = True

            start_date = date

            start_equity = closed_equity

            bars = 0


        # --------------------------
        # Campaign continues
        # --------------------------

        if active:

            bars += 1


        # --------------------------
        # Campaign ends
        # --------------------------

        if active and not portfolio_active:

            end_equity = closed_equity

            return_pct = (

                end_equity

                /

                start_equity

                - 1

            )


            campaigns.append(

                Campaign(

                    start_date=start_date,

                    end_date=date,

                    start_equity=start_equity,

                    end_equity=end_equity,

                    return_pct=return_pct,

                    bars_held=bars,

                    winning_campaign=(
                        return_pct > 0
                    ),

                )

            )


            active = False

            start_date = None

            start_equity = None

            bars = 0


    return campaigns