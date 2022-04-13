import pytest

from datetime_format import (
    dtfmt,
    dtformat,
    DateTimeFormatter,
    DateTimeFormatTimeZoneError,
    DateTimeFormatFieldError,
    DateTimeFormatTranslationError,
)
from datetime_format.__formats import _SUPPORTED_DATETIME_OUTPUT_FORMATS
from datetime import date, datetime, timezone
import holidays

def test_formatter_input():
    assert DateTimeFormatter(20050301).dt.dt == datetime(2005, 3, 1)
    assert DateTimeFormatter(200503).dt.dt == datetime(2005, 3, 1)
    assert DateTimeFormatter("2005-03-01").dt.dt == datetime(2005, 3, 1)
    assert DateTimeFormatter(
        "2005-03-01 08:31:25"
    ).dt.dt == datetime(2005, 3, 1, 8, 31, 25)
    assert DateTimeFormatter(
        "2005-03-01T05:00:00-00:00"
    ).dt.dt == datetime(2005, 3, 1, 5, 0, 0, tzinfo=timezone.utc)

def test_formatter_basic():
    dtf = DateTimeFormatter(20050301)

    # test use of __call__
    dtf("%YYYYMMDD%") == "20050301"

    # tests both upper and lowercase usage
    for k, fmt in _SUPPORTED_DATETIME_OUTPUT_FORMATS.items():
        if isinstance(fmt, str):
            assert dtf.format(f"%{k}%") == dtf.dt.dt.strftime(fmt)
        else:
            assert dtf.format(f"%{k}%") == fmt(dtf.dt.dt)

def test_formatter_with_addl():
    dtf = DateTimeFormatter(20050301)
    assert dtf.format("{}", 111) == "111"
    assert dtf.format("%YYYYMMDD") == "%YYYYMMDD"
    assert dtf.format("xxx %YYYYMMDD%") == "xxx 20050301"
    assert dtf.format("xxx %YYYYMMDD% %MMDDYYYY%") == "xxx 20050301 03012005"
    assert dtf.format("{0} %YYYYMMDD%", "yyy") == "yyy 20050301"

def test_formatter_with_date_translation():
    dtf = DateTimeFormatter(20050301)
    assert dtf.format("%YYYYMMDD-M1D%") == "20050228"
    assert dtf.format("%YYYYMMDD-M1m%") == "20050201"
    assert dtf.format("%YYYYMMDD-M1Y%") == "20040301"
    assert dtf.format("%YYYYMMDD-m1D%") == "20050228"
    assert dtf.format("%YYYYMMDD-m1m%") == "20050201"
    assert dtf.format("%YYYYMMDD-m1Y%") == "20040301"
    assert dtf.format("%YYYYMMDD-P1D%") == "20050302"
    assert dtf.format("%YYYYMMDD-P1m%") == "20050401"
    assert dtf.format("%YYYYMMDD-P1Y%") == "20060301"
    assert dtf.format("%YYYYMMDD-p1D%") == "20050302"
    assert dtf.format("%YYYYMMDD-p1m%") == "20050401"
    assert dtf.format("%YYYYMMDD-p1Y%") == "20060301"
    assert dtf.format("%YYYYMMDD-p1Y%") == "20060301"

    ## test multi period
    assert dtf.format("%YYYYMMDD-m20Y%") == "19850301"
    assert dtf.format("%YYYYMMDD-p10Y%") == "20150301"

    ## test business days / holidays
    dtf = DateTimeFormatter(20050502, holidays.US()) # Monday
    assert dtf.format("%YYYYMMDD-M1B%") == "20050429"
    assert dtf.format("%YYYYMMDD-P10B%") == "20050516"
    assert dtf.format("%YYYYMMDD-P28D%") == "20050531"

def test_formatter_with_time_translation():
    dtf = DateTimeFormatter("2005-03-01 23:59:59.111")
    assert dtf.format("%YYYYMMDD-P1M%") == "20050302"
    assert dtf.format(
        "%YYYYMMDD-P889000Z% %HHMMSSZZ-P889000Z%"
    ) == "20050302 00:00:00.000000"
    assert dtf.format("%HHMMSS-P1M%") == "00:00:59"
    assert dtf.format("%HHMMSSZZ-P1M%") == "00:00:59.111000"
    assert dtf.format("%HHMMSS-M1H%") == "22:59:59"

def test_formatter_with_assert():
    dtf = DateTimeFormatter(20050301)
    with pytest.raises(DateTimeFormatFieldError):
        dtf.format("%NOT_EXIST-M1D%")
    with pytest.raises(DateTimeFormatTranslationError):
        dtf.format("%YYYYMMDD-X1D%")
    with pytest.raises(DateTimeFormatTranslationError):
        dtf.format("%YYYYMMDD-PXD%")
    with pytest.raises(DateTimeFormatTranslationError):
        dtf.format("%YYYYMMDD-P1Q%")
    with pytest.raises(DateTimeFormatTimeZoneError):
        dtfmt(20050301, "HHMMSS", output_tz=timezone.utc)
    with pytest.raises(DateTimeFormatTimeZoneError):
        dtfmt(20050301, "HHMMSS", output_tz="not_a_tz")


def test_dtfmt():
    assert dtformat(20050301, None) is None
    assert dtformat(20050301, "YYYYMMDD") == "20050301"
    assert dtfmt(20050301, "YYYYMMDD") == "20050301"
    assert dtfmt(20050301, "%YYYYMMDD%") == "20050301"
    assert dtfmt("2005-03-01", "YYYYMMDD") == "20050301"
    assert dtfmt(date(2005, 3, 1), "YYYYMMDD") == "20050301"
    assert dtfmt(datetime(2005, 3, 1), "YYYYMMDD") == "20050301"
    assert dtfmt(
        "2005-03-01T05:00:00-05:00", "HHMMSS", timezone.utc,
    ) == "10:00:00"
    assert dtfmt(
        "2005-03-01T05:00:00-05:00", "HHMMSS", "utc",
    ) == "10:00:00"

    test_holiday = {"2007-01-01": "NYD"}
    assert dtfmt(20061229, "DATE-P2B", holidays=test_holiday) == "2007-01-03"
