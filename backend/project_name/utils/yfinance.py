from datetime import datetime
from datetime import timedelta


def convert_timeframe_to_period(timeframe: str):
    if timeframe == "1D":
        return "1d", "5m"
    elif timeframe == "1W":
        return "5d", "30m"
    elif timeframe == "1M":
        return "1mo", "90m"
    elif timeframe == "3M":
        return "3mo", "1d"
    elif timeframe == "YTD":
        return "ytd", "1d"
    elif timeframe == "1Y":
        return "1y", "1d"
    elif timeframe == "ALL":
        return "max", "1wk"
    else:
        raise ValueError("Invalid timeframe")


def interval_from_start_date(start_date: datetime):
    today = datetime.now()
    delta = today - start_date

    if delta.days < 2:
        return "5m"
    elif delta.days < 7:
        return "30m"
    elif delta.days < 30:
        return "90m"
    elif delta.days < 365:
        return "1d"
    else:
        return "1w"


def format_date(date: datetime, timeframe: str):
    if timeframe == "1D":
        return date.strftime("%-I:%M %p")
    elif timeframe == "1W" or timeframe == "1M":
        return date.strftime("%m/%d %-I:%M %p")
    else:
        return date.strftime("%m/%d/%Y")


def get_start_from_timeframe(timeframe: str) -> datetime:
    time = datetime.now() - _timeframe_to_timedelta(timeframe)
    time.replace(hour=0, minute=0, second=0, microsecond=0)
    return time


def _timeframe_to_timedelta(timeframe: str) -> timedelta:
    if timeframe == "1D":
        return timedelta(days=1)
    if timeframe == "1W":
        return timedelta(weeks=1)
    if timeframe == "1M":
        return timedelta(weeks=4)
    if timeframe == "3M":
        return timedelta(weeks=12)
    if timeframe == "YTD":
        return timedelta(weeks=datetime.now().isocalendar()[1])
    if timeframe == "1Y":
        return timedelta(weeks=52)
    if timeframe == "ALL":
        return datetime.now() - datetime(1970, 1, 1)
