import exchange_calendars as xcals
from datetime import datetime
import pytz


def latest_market_date():

    nyse = xcals.get_calendar("XNYS")

    eastern = pytz.timezone("America/New_York")

    today = datetime.now(eastern).date()

    sessions = nyse.sessions_in_range(
        "2006-07-24",
        today,
    )

    return sessions[-1].date().isoformat()


if __name__ == "__main__":
    print(latest_market_date())
