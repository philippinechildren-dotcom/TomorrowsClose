from datetime import datetime

from dateutil.relativedelta import relativedelta


def rolling_one_year(today: datetime) -> tuple:
    """
    Return the nominal rolling one-year reporting window.

    The returned dates are adjusted later by
    rolling_window.filter_complete_positions().
    """

    start_date = today - relativedelta(years=1)

    end_date = today

    return start_date, end_date


def rolling_six_months(today: datetime) -> tuple:
    """
    Return the nominal rolling six-month reporting window.
    """

    start_date = today - relativedelta(months=6)

    end_date = today

    return start_date, end_date


def year_to_date(today: datetime) -> tuple:
    """
    Return the current calendar year reporting window.
    """

    start_date = datetime(
        year=today.year,
        month=1,
        day=1,
    )

    end_date = today

    return start_date, end_date


def since_inception(first_trade_date: datetime,
                    today: datetime) -> tuple:
    """
    Return the full reporting window.
    """

    return first_trade_date, today