from datetime import datetime

from dateutil.relativedelta import relativedelta


def get_reporting_window(
    today: datetime,
    period: str = "1y",
) -> tuple:
    """
    Return the requested reporting window.

    Supported periods:

        ytd
        1y
        3y
        5y
        10y
        all

    The returned dates are adjusted later by
    filter_complete_positions().
    """

    end_date = today

    if period == "ytd":

        start_date = today.replace(
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

    elif period == "1y":

        start_date = today - relativedelta(years=1)

    elif period == "3y":

        start_date = today - relativedelta(years=3)

    elif period == "5y":

        start_date = today - relativedelta(years=5)

    elif period == "10y":

        start_date = today - relativedelta(years=10)

    elif period == "all":

        start_date = None

    else:

        raise ValueError(
            f"Unknown reporting period: {period}"
        )

    return start_date, end_date