from datetime import datetime

from dateutil.relativedelta import relativedelta


class BarArgs:
    def __init__(self, timeframe: str, multiplier: int, from_: datetime, to: datetime):
        self.timeframe = timeframe
        self.multiplier = multiplier
        self.from_ = from_.strftime("%Y-%m-%d")
        self.to = to.strftime("%Y-%m-%d")


def timeframe_to_bar(timeframe: str) -> BarArgs:
    """
    Transform a timeframe (1D, 1W, 1M, 3M, YTD, 1Y, ALL) into arguments for the Polygon Bar API.

    :param timeframe: The timeframe.
    :return: A tuple of timeframe and multiplier.
    """

    to = get_last_business_day(datetime.now())

    if timeframe == "1D":
        return BarArgs(
            timeframe="minute",
            multiplier=5,
            from_=datetime(to.year, to.month, to.day),
            to=to,
        )
    elif timeframe == "1W":
        return BarArgs(
            timeframe="hour",
            multiplier=1,
            from_=get_last_business_day(to - relativedelta(weeks=1)),
            to=to,
        )
    elif timeframe == "1M":
        return BarArgs(
            timeframe="day",
            multiplier=1,
            from_=get_last_business_day(to - relativedelta(months=1)),
            to=to,
        )
    elif timeframe == "3M":
        return BarArgs(
            timeframe="day",
            multiplier=1,
            from_=get_last_business_day(to - relativedelta(months=3)),
            to=to,
        )
    elif timeframe == "YTD":
        return BarArgs(
            timeframe="day",
            multiplier=1,
            from_=get_last_business_day(datetime(to.year, 1, 1)),
            to=to,
        )
    elif timeframe == "1Y":
        return BarArgs(
            timeframe="day",
            multiplier=1,
            from_=get_last_business_day(to - relativedelta(years=1)),
            to=to,
        )
    elif timeframe == "ALL":
        return BarArgs(
            timeframe="day",
            multiplier=1,
            from_=get_last_business_day(datetime.fromtimestamp(0)),
            to=to,
        )
    else:
        raise ValueError("Invalid timeframe")


def get_last_business_day(date: datetime):
    """
    Get the last business day.
    """
    # If the date is a weekend, get the last Friday.
    if date.weekday() >= 5:
        date -= relativedelta(days=date.weekday() - 4)

    # If the date is a weekday, check if it's a holiday.
    if date.strftime("%Y-%m-%d") in [
        "2024-01-01",  # New Year's Day
        "2024-01-15",  # MLK Day
        "2024-02-19",  # President's Day
        "2024-05-27",  # Memorial Day
        "2024-06-19",  # Juneteenth
        "2024-07-04",  # Independence Day
        "2024-09-02",  # Labor Day
        "2024-10-14",  # Columbus Day
        "2024-11-11",  # Veteran's Day
        "2024-11-28",  # Thanksgiving
        "2024-12-25",  # Christmas
    ]:
        date -= relativedelta(days=1)

    return date
