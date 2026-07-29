from datetime import datetime
from zoneinfo import ZoneInfo


def add_common_page_data(
    result,
    strategy,
    history,
    indicator=None,
):

    market_date = history.index[-1].strftime(
        "%B %d, %Y"
    )

    calculation_time = (
        datetime.now(
            ZoneInfo("America/New_York")
        )
        .strftime("%I:%M %p ET")
    )

    result.update({

        "data_confidence": "★★★★★",

        "data_source": "Yahoo Finance",

        "last_updated": market_date,

        "last_updated_time": calculation_time,

        "strategy": strategy,

    })

    if indicator is not None:

        result["indicator"] = indicator

    return result