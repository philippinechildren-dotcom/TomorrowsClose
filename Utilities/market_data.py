"""
Utilities/market_data.py

Market data for Tomorrow's Close.

This module is the only part of the application that knows
where market data comes from.
"""

from datetime import datetime, timedelta
from time import sleep
from zoneinfo import ZoneInfo

import pandas as pd
import pandas_market_calendars as mcal
import yfinance as yf

SETTLEMENT_DELAY_MINUTES = 30
DATA_REFRESH_DELAY_MINUTES = 25
DATA_REFRESH_RETRIES = 3
DATA_REFRESH_RETRY_DELAY_SECONDS = 2

_market_history_cache = {}
_market_refresh_attempted = {}


def _nasdaq_calendar():
    return mcal.get_calendar("NASDAQ")


def _market_session_complete(date):
    """Returns True when the NASDAQ trading session has completed."""
    calendar = _nasdaq_calendar()
    schedule = calendar.schedule(start_date=date, end_date=date)

    if schedule.empty:
        return False

    close_time = schedule.iloc[0]["market_close"].tz_convert(
        "America/New_York"
    )
    current_time = datetime.now(ZoneInfo("America/New_York"))

    return current_time >= close_time


def _market_state():
    """
    Returns the current market-data state.

    current:
        Normal operation.

    settlement:
        Between the official market close and the end of the
        30-minute settlement period.
    """
    current_time = datetime.now(ZoneInfo("America/New_York"))
    calendar = _nasdaq_calendar()
    schedule = calendar.schedule(
        start_date=current_time.date(),
        end_date=current_time.date(),
    )

    if schedule.empty:
        return "current"

    close_time = schedule.iloc[0]["market_close"].tz_convert(
        "America/New_York"
    )
    settlement_complete = close_time + timedelta(
        minutes=SETTLEMENT_DELAY_MINUTES
    )

    if close_time <= current_time < settlement_complete:
        return "settlement"

    return "current"


def _latest_expected_session_date():
    """
    Returns the latest NASDAQ session for which a completed
    daily bar should currently be available.
    """
    current_time = datetime.now(ZoneInfo("America/New_York"))
    calendar = _nasdaq_calendar()

    today_schedule = calendar.schedule(
        start_date=current_time.date(),
        end_date=current_time.date(),
    )

    if not today_schedule.empty:
        close_time = today_schedule.iloc[0]["market_close"].tz_convert(
            "America/New_York"
        )

        if current_time >= close_time:
            return current_time.date()

    previous_schedule = calendar.schedule(
        start_date=current_time.date() - timedelta(days=10),
        end_date=current_time.date(),
    )

    if previous_schedule.empty:
        return None

    return previous_schedule.index[-1].date()


def _data_refresh_window_open():
    """
    Returns True when it is time to begin looking for the new
    daily market bar.

    The refresh window begins 25 minutes after the official
    NASDAQ close, normally 4:25 PM ET.
    """
    current_time = datetime.now(ZoneInfo("America/New_York"))
    calendar = _nasdaq_calendar()
    schedule = calendar.schedule(
        start_date=current_time.date(),
        end_date=current_time.date(),
    )

    if schedule.empty:
        return False

    close_time = schedule.iloc[0]["market_close"].tz_convert(
        "America/New_York"
    )
    refresh_time = close_time + timedelta(
        minutes=DATA_REFRESH_DELAY_MINUTES
    )

    return current_time >= refresh_time


def _remove_incomplete_daily_bar(history):
    """Removes today's bar if the trading session has not finished."""
    if history.empty:
        return history

    latest_date = history.index[-1].date()

    if not _market_session_complete(latest_date):
        return history.iloc[:-1]

    return history


def _has_valid_latest_completed_bar(history):
    """Returns True when the latest completed bar has valid data."""
    if history.empty:
        return False

    history = _remove_incomplete_daily_bar(history)

    if history.empty:
        return False

    latest_bar = history.iloc[-1]

    for column in ["Open", "High", "Low", "Close", "Volume"]:
        if column not in history.columns:
            return False

        if pd.isna(latest_bar[column]):
            return False

    return True


def _download_full_history(ticker):
    """Download complete available daily history."""
    stock = yf.Ticker(ticker)

    history = stock.history(
        period="max",
        interval="1d",
        auto_adjust=False,
        repair=False,
        prepost=False,
    )

    if history.empty:
        raise ValueError(
            f"No market data found for ticker '{ticker}'."
        )

    return history


def _download_current_history(ticker):
    """Download recent daily history for current-bar validation."""
    stock = yf.Ticker(ticker)

    history = stock.history(
        period="5d",
        interval="1d",
        auto_adjust=False,
        repair=False,
        prepost=False,
    )

    if history.empty:
        raise ValueError(
            f"No market data found for ticker '{ticker}'."
        )

    latest_date = history.index[-1].date()
    if _market_session_complete(latest_date):
        latest_close = history.iloc[-1]["Close"]

        if pd.isna(latest_close):
            regular_market_price = stock.history_metadata.get(
                "regularMarketPrice"
            )

            if regular_market_price is not None:
                history.loc[history.index[-1], "Close"] = float(
                    regular_market_price
                )

    return history

def _store_history(ticker, history):
    """Validate, normalize, and store full history in the cache."""
    history = _remove_incomplete_daily_bar(history)

    if not _has_valid_latest_completed_bar(history):
        return False

    history = history.rename(
        columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        }
    )

    history = history[
        ["open", "high", "low", "close", "volume"]
    ]

    _market_history_cache[ticker] = history.round(2)

    return True


def _refresh_history_if_needed(ticker):
    """
    Refresh the cached full history when a new trading session
    should be available.

    The existing cache is never replaced by invalid Yahoo data.

    Returns True when valid current data is available.
    """
    ticker = ticker.upper()
    expected_date = _latest_expected_session_date()

    if expected_date is None:
        return False

    cached_history = _market_history_cache.get(ticker)

    if cached_history is not None and not cached_history.empty:
        if cached_history.index[-1].date() >= expected_date:
            return True

    if not _data_refresh_window_open():
        return cached_history is not None and not cached_history.empty

    for attempt in range(DATA_REFRESH_RETRIES):
        _market_refresh_attempted[ticker] = expected_date

        try:
            recent_history = _download_current_history(ticker)
            recent_history = _remove_incomplete_daily_bar(
                recent_history
            )

            if not recent_history.empty:
                latest_date = recent_history.index[-1].date()
                latest_close = recent_history.iloc[-1]["Close"]

                if (
                    latest_date >= expected_date
                    and not pd.isna(latest_close)
                ):
                    full_history = _download_full_history(ticker)

                    matching_rows = full_history.index.date == latest_date

                    if matching_rows.any():
                        latest_index = full_history.index[matching_rows][-1]

                        if pd.isna(
                            full_history.loc[latest_index, "Close"]
                        ):
                            full_history.loc[
                                latest_index, "Close"
                            ] = latest_close

                    if _store_history(ticker, full_history):
                        if (
                            _market_history_cache[ticker].index[-1].date()
                            >= expected_date
                        ):
                            return True
        except Exception:
            pass

        if attempt < DATA_REFRESH_RETRIES - 1:
            sleep(DATA_REFRESH_RETRY_DELAY_SECONDS)

    return False

def get_market_data(ticker):
    """
    Returns the latest completed daily market data.

    If a new daily bar is expected but Yahoo has not supplied
    a valid one, market_state is 'invalid_data'.
    """
    ticker = ticker.upper()
    state = _market_state()
    refresh_successful = _refresh_history_if_needed(ticker)
    history = _market_history_cache.get(ticker)
    expected_date = _latest_expected_session_date()

    if history is None or history.empty:
        try:
            full_history = _download_full_history(ticker)

            if not _store_history(ticker, full_history):
                raise ValueError(
                    f"Latest market data for '{ticker}' is invalid."
                )

            history = _market_history_cache[ticker]
        except Exception as error:
            raise ValueError(
                f"Valid market data is not currently available "
                f"for ticker '{ticker}'."
            ) from error

    cached_date = history.index[-1].date()

    if (
        expected_date is not None
        and cached_date < expected_date
        and _data_refresh_window_open()
        and not refresh_successful
    ):
        state = "invalid_data"

    if _market_state() == "settlement":
        state = "settlement"

    latest_bar = history.iloc[-1]

    last_updated = datetime.now(
        ZoneInfo("America/New_York")
    ).strftime("%B %d, %Y %I:%M %p ET")

    return {
        "ticker": ticker,
        "date": str(cached_date),
        "open": round(float(latest_bar["open"]), 2),
        "high": round(float(latest_bar["high"]), 2),
        "low": round(float(latest_bar["low"]), 2),
        "close": round(float(latest_bar["close"]), 2),
        "volume": int(latest_bar["volume"]),
        "source": "Yahoo Finance",
        "last_updated": last_updated,
        "market_state": state,
    }


def get_market_history(ticker, number_of_bars=None):
    """
    Returns completed historical daily market data.

    If Yahoo fails to provide a new bar, the existing validated
    cache remains available internally. get_market_data() reports
    the invalid_data state so the PriceSolver cannot display a
    stale signal.
    """
    ticker = ticker.upper()

    _refresh_history_if_needed(ticker)

    history = _market_history_cache.get(ticker)

    if history is None or history.empty:
        full_history = _download_full_history(ticker)

        if not _store_history(ticker, full_history):
            raise ValueError(
                f"Valid market data is not currently available "
                f"for ticker '{ticker}'."
            )

        history = _market_history_cache[ticker]

    history = history.copy()

    if number_of_bars is not None:
        history = history.tail(number_of_bars)

    return history


def get_market_data_state(ticker):
    """Returns current, settlement, or invalid_data."""
    ticker = ticker.upper()
    state = _market_state()

    if state == "settlement":
        return state

    history = _market_history_cache.get(ticker)

    if history is None or history.empty:
        _refresh_history_if_needed(ticker)
        history = _market_history_cache.get(ticker)

    if history is None or history.empty:
        return "invalid_data"

    expected_date = _latest_expected_session_date()

    if (
        expected_date is not None
        and history.index[-1].date() < expected_date
        and _data_refresh_window_open()
    ):
        if not _refresh_history_if_needed(ticker):
            return "invalid_data"

        history = _market_history_cache.get(ticker)

        if (
            history is None
            or history.empty
            or history.index[-1].date() < expected_date
        ):
            return "invalid_data"

    return "current"


def filter_history(history, period=None):
    """
    Filter market history.

    period:
        None
        "1_month"
        "3_months"
        "6_months"
        "ytd"
        "1_year"
        "2_years"
        "3_years"
        "5_years"
        "10_years"
        "maximum"
    """
    if period is None or period == "maximum":
        return history

    if period == "ytd":
        current_year = datetime.now(
            ZoneInfo("America/New_York")
        ).year

        return history[
            history.index.year == current_year
        ]

    if isinstance(period, str):
        period_lookup = {
            "1_month": 1 / 12,
            "3_months": 0.25,
            "6_months": 0.5,
            "1_year": 1,
            "2_years": 2,
            "3_years": 3,
            "5_years": 5,
            "10_years": 10,
        }

        period = period_lookup[period]
    else:
        period = float(period)

    performance_days = int(252 * period)

    if len(history) <= performance_days:
        return history

    return history.iloc[-performance_days:]