from datetime import datetime


def format_price(price: float) -> str:
    """
    Format a price for display.
    Future versions can support tick-size metadata
    or variable decimal precision.
    """

    return f"{price:.2f}"


def format_date(date: datetime) -> str:
    """
    Format a market date.
    """

    return date.strftime(
        "%B %d, %Y"
    )


def format_time(date: datetime) -> str:
    """
    Format an Eastern Time timestamp.
    """

    return date.strftime(
        "%I:%M %p ET"
    )