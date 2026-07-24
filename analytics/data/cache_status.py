from datetime import datetime, UTC
from analytics.data.market_status import latest_market_date


def get_cache_status(cached_market_date):

    latest = latest_market_date()

    if cached_market_date == latest:
        return "current"

    return "stale"


def build_status(cached_market_date):

    return {
        "last_checked": datetime.now(UTC).isoformat(),
        "market_date": cached_market_date,
        "latest_market_date": latest_market_date(),
        "data_status": get_cache_status(cached_market_date),
    }
