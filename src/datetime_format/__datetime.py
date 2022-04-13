
import datetime

from .__formats import *

def _date_to_datetime(date):
    return datetime.datetime.combine(
        date,
        datetime.time(hour=0, minute=0, second=0, microsecond=0),
        tzinfo=None
    )

def _try_yyyy_mm_dd(fields):
    if len(fields[0]) != 4:
        return None
    yyyy = int(fields[0])
    mm = int(fields[1])
    dd = int(fields[2])
    return datetime.date(year=yyyy, month=mm, day=dd)

def _try_end_yyyy(fields):
    if len(fields[2]) != 4:
        return None
    yyyy = int(fields[2])
    mm = int(fields[0])
    dd = int(fields[1])
    if mm > 12:
        # must be dd-mm, so swap mm and dd
        return datetime.date(year=yyyy, month=dd, day=mm)
    return datetime.date(year=yyyy, month=mm, day=dd)

def _try_end_yy(fields):
        if len(fields[2]) != 2:
            return None
        yy = int(fields[2])
        mm = int(fields[0])
        dd = int(fields[1])
        yyyy = yy + 2000
        if yy > _DATE_SWITCHOVER:
            yyyy = yy + 1900
        if mm > 12:
            # must be dd-mm, so swap mm and dd
            return datetime.date(year=yyyy, month=dd, day=mm)
        return datetime.date(year=yyyy, month=mm, day=dd)

def _convert_non_isostring_to_datetime(s):
    for sc in _DATE_SPLIT_CHARS:
        fields = s.split(sc)
        fields_len = len(fields)
        if fields_len == 3:
            break
        if fields_len == 2 or fields_len > 3:
            raise ValueError(
                "invalid date format used ({s}), must be one of:\n"
                f"{', '.join(_SUPPORTED_DATE_FORMATS)}"
            )
    if len(fields) != 3:
        raise ValueError(
            f"invalid date format used, could not find split char in ({s}), "
            f"format must be one of:\n{', '.join(_SUPPORTED_DATE_FORMATS)}"
        )
    date = _try_yyyy_mm_dd(fields)
    if date is None:
        date = _try_end_yyyy(fields)
    if date is None:
        date = _try_end_yy(fields)
    return _date_to_datetime(date)

def _string_to_dt(s):
    # no other 8 char meaning
    if len(s) == 8:
        try:
            return _int_to_dt(int(s))
        except ValueError:
            pass
    try:
        return _date_to_datetime(datetime.date.fromisoformat(s))
    except ValueError:
        if ":" in s:
            # support date times, not just dates
            pass
        # this can be one of many types of date, but cannot be a datetime
        # e.g. ISO (YYYY-MM-DD), non-ISO: (YYYY/MM/DD, MM/DD/YYYY)
        # The above are the three formats we support
        return _convert_non_isostring_to_datetime(s)


def _int_to_dt(i):
    _min_allowed = 10000000
    if i < _min_allowed:
        raise ValueError(
            f"integer date {i} smaller than min allowed ({_min_allowed})"
        )
    # convert YYYY to <YYYY>MMDD multiply by 1000, then add biggest MMDD possible
    _max_allowed = datetime.MAXYEAR*10000 + 1231
    if i > _max_allowed:
        raise ValueError(
            f"integer date {i} greater than max allowed (){_max_allowed})"
        )
    yyyy = i // 10000
    mm = (i - yyyy*10000) // 100
    dd = i - yyyy*10000 - mm*100
    return _date_to_datetime(
        datetime.date(year=yyyy, month=mm, day=dd),
    )

class _DateTime():
    def __init__(self, arg=None):
        self.dt = None
        if arg is None:
            self.dt = datetime.datetime.now()
        if isinstance(arg, str):
            self.dt = _string_to_dt(arg)
        if isinstance(arg, int):
            self.dt = _int_to_dt(arg)
        if self.dt is None:
            raise ValueError(
                f"invalid datetime {arg} provided, could not process"
            )
