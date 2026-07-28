from datetime import datetime
from zoneinfo import ZoneInfo


def add_page_data(result, strategy, history, indicator):
    result["data_confidence"] = "★★★★★"
    result["data_source"] = "Yahoo Finance"
    result["last_updated"] = history.index[-1].strftime("%B %d, %Y")
    result["last_updated_time"] = datetime.now(
        ZoneInfo("America/New_York")
    ).strftime("%I:%M %p ET")
    result["strategy"] = strategy
    result["indicator"] = indicator

    return result