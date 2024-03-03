import calendar
import datetime
import enum
from typing import (
    Dict,
    Optional,
    Tuple,
    Union,
)

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

from dateutil import relativedelta

LOCAL_TZ: ZoneInfo = ZoneInfo("Asia/Bangkok")

DATETIME_SET: Tuple[str, ...] = (
    "year",
    "month",
    "day",
    "hour",
    "minute",
    "second",
    "microsecond",
)


def get_datetime_replace(
    year: Optional[int] = None,
    month: Optional[int] = None,
) -> Dict[str, tuple]:
    return {
        "year": (1990, 9999),
        "month": (1, 12),
        "day": (
            1,
            (calendar.monthrange(year, month)[1] if year and month else 31),
        ),
        "hour": (0, 23),
        "minute": (0, 59),
        "second": (0, 59),
        "microsecond": (0, 999999),
    }


class DatetimeDim(enum.IntEnum):
    """Datetime dimension enumerations"""

    MICROSECOND = 0
    SECOND = 1
    MINUTE = 2
    HOUR = 3
    DAY = 4
    MONTH = 5
    YEAR = 6


def now(_tz: Optional[str] = None):
    _tz: ZoneInfo = ZoneInfo(_tz) if _tz and isinstance(_tz, str) else LOCAL_TZ
    return datetime.datetime.now(_tz)


def get_date(
    fmt: str,
    *,
    _tz: Optional[str] = None,
) -> Union[datetime.datetime, datetime.date, str]:
    """
    Examples:
        >>> get_date(fmt='%Y-%m-%d')
        '2023-01-01'
    """
    _datetime: datetime.datetime = now(_tz)
    if fmt == "datetime":
        return _datetime
    elif fmt == "date":
        return _datetime.date()
    return _datetime.strftime(fmt)


def replace_date(
    dt: datetime.datetime, mode: str, reverse: bool = False
) -> datetime.datetime:
    """
    Examples:
        >>> replace_date(datetime.datetime(2023, 1, 31, 13, 2, 47), mode='day')
        datetime.datetime(2023, 1, 31, 0, 0)
    """
    assert mode in {"month", "day", "hour", "minute", "second", "microsecond"}
    replace_mapping: Dict[str, tuple] = get_datetime_replace(dt.year, dt.month)
    return dt.replace(
        **{
            _.name.lower(): replace_mapping[_.name.lower()][int(reverse)]
            for _ in DatetimeDim
            if _ < DatetimeDim[mode.upper()]
        }
    )


def next_date(
    dt: datetime.datetime,
    mode: str,
    *,
    reverse: bool = False,
    next_value: int = 1,
) -> datetime.datetime:
    """
    Examples:
        >>> next_date(datetime.datetime(2023, 1, 31, 0, 0, 0), mode='day')
        datetime.datetime(2023, 2, 1, 0, 0)
        >>> next_date(datetime.datetime(2023, 1, 31, 0, 0, 0), mode='month')
        datetime.datetime(2023, 2, 28, 0, 0)
        >>> next_date(datetime.datetime(2023, 1, 31, 0, 0, 0), mode='hour')
        datetime.datetime(2023, 1, 31, 1, 0)
    """
    assert mode in {"month", "day", "hour", "minute", "second", "microsecond"}
    return dt + relativedelta.relativedelta(
        **{f"{mode}s": (-next_value if reverse else next_value)}
    )
