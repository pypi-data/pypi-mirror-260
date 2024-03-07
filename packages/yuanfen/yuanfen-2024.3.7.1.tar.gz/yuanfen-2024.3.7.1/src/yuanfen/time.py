import time
from datetime import datetime

import pytz


def now():
    return datetime.now()


def format(dt: datetime = None, format: str = "%Y-%m-%dT%H:%M:%S.%f") -> str:
    if dt is None:
        dt = now()
    return dt.strftime(format)


def parse(dt_str: str, format: str = "%Y-%m-%dT%H:%M:%S.%f") -> datetime:
    return datetime.strptime(dt_str, format)


def remove_tz(dt: datetime, tz: str = "Asia/Shanghai") -> datetime:
    if dt.tzinfo is None:
        return dt
    timezone = pytz.timezone(tz)
    return dt.astimezone(timezone).replace(tzinfo=None)


def format_duration(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"


def sleep(secs: float):
    time.sleep(secs)
