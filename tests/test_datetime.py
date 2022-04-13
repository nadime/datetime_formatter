import pytest
import datetime
from dateutil.relativedelta import relativedelta as rd
import holidays

from datetime_format.__datetime import (
    _int_to_datetime,
    _string_to_datetime,
    _DateTime,
)

1
def test_int_to_datetime():
    assert _int_to_datetime(20050102) == datetime.datetime(2005, 1, 2)
    assert _int_to_datetime(19050102) == datetime.datetime(1905, 1, 2)
    assert _int_to_datetime(18050102) == datetime.datetime(1805, 1, 2)
    assert _int_to_datetime(184530) == (
            datetime.datetime.combine(
                datetime.date.today(), datetime.time(18, 45, 30)
            ))
    assert _int_to_datetime(194530) == (
            datetime.datetime.combine(
                datetime.date.today(), datetime.time(19, 45, 30)
            ))
    assert _int_to_datetime(200503) == datetime.datetime(2005, 3, 1)
    assert _int_to_datetime(199903) == datetime.datetime(1999, 3, 1)
    assert _int_to_datetime(251111) == datetime.datetime(2511, 11,1)

    with pytest.raises(ValueError):
        _int_to_datetime(206132)
    with pytest.raises(ValueError):
        _int_to_datetime(251332)
    with pytest.raises(ValueError):
        _int_to_datetime(113065)
    with pytest.raises(ValueError):
        _int_to_datetime(1130051)



def test_string_to_datetime_date():
    assert _string_to_datetime("20050102") == datetime.datetime(2005, 1, 2)
    assert _string_to_datetime("2005-01-02") == datetime.datetime(2005, 1, 2)
    assert _string_to_datetime("2005/01/02") == datetime.datetime(2005, 1, 2)
    assert _string_to_datetime("01-02-2005") == datetime.datetime(2005, 1, 2)
    assert _string_to_datetime("10-01-65") == datetime.datetime(2065, 10, 1)
    assert _string_to_datetime("10-01-66") == datetime.datetime(1966, 10, 1)
    assert _string_to_datetime("25-10-2005") == datetime.datetime(2005, 10, 25)
    assert _string_to_datetime("25-10-66") == datetime.datetime(1966, 10, 25)

    with pytest.raises(ValueError):
        _string_to_datetime("20050102 18:30 11")
    with pytest.raises(ValueError):
        _string_to_datetime("101")

def _combine_time(t):
    return datetime.datetime.combine(
        datetime.datetime.today(),
        t,
    )

def test_string_to_datetime_time():
    assert _string_to_datetime("08:30:15") == _combine_time(datetime.time(8,30,15))
    assert _string_to_datetime("14:21:27.13") == _combine_time(datetime.time(14,21,27,130000))
    assert _string_to_datetime("19:47:38.131010") == _combine_time(datetime.time(19,47,38,131010))
    assert _string_to_datetime("19:47") == _combine_time(datetime.time(19,47,0))
    assert _string_to_datetime("8:47") == _combine_time(datetime.time(8,47,0))
    assert _string_to_datetime("13:15:00.999999") == _combine_time(datetime.time(13,15,0,999999))
    with pytest.raises(ValueError):
        _string_to_datetime("13:15:00.9999999")

def test_string_to_datetime_combined():
    assert _string_to_datetime("2005-03-01 08:03:30.111") == (
        datetime.datetime(2005, 3, 1, 8, 3, 30, 111000)
    )
    assert _string_to_datetime("2005-03-01 08:03:30") == (
        datetime.datetime(2005,3,1,8,3,30)
    )
    assert _string_to_datetime("1905-03-01 13:03:30.11") == (
        datetime.datetime(1905,3,1,13,3,30,110000)
    )
    assert _string_to_datetime("2005-03-01 83011") == (
        datetime.datetime(2005,3,1,8,30,11)
    )
    with pytest.raises(ValueError):
        _string_to_datetime("2005-03 08:03:30")
    with pytest.raises(ValueError):
        _string_to_datetime("2005-03-01 25:03:30")
    with pytest.raises(ValueError):
        _string_to_datetime("113161")
    with pytest.raises(ValueError):
        _string_to_datetime("193161")


class _hastodt():
    def __init__(self, dt):
        self.dt = dt
    def to_datetime(self):
        return self.dt

def test_datetime_class():
    assert _DateTime().dt.year == datetime.datetime.now().year
    assert _DateTime("200503").dt == datetime.datetime(2005, 3, 1)
    assert _DateTime("20050301").dt == datetime.datetime(2005, 3, 1)
    assert _DateTime("08:30:10").dt == _combine_time(datetime.time(8, 30, 10))
    assert _DateTime(
        datetime.datetime(2005, 3, 1)
    ).dt == datetime.datetime(2005, 3, 1)
    assert _DateTime(
        datetime.date(2005, 3, 1)
    ).dt == datetime.datetime(2005, 3, 1)
    assert _DateTime(
        datetime.time(18, 30, 10)
    ).dt == datetime.datetime.combine(
        datetime.datetime.today(),
        datetime.time(18, 30, 10)
    )
    assert _DateTime("2005-03-01 08:30:10").dt == (
        datetime.datetime(2005, 3, 1, 8, 30, 10)
    )
    assert _DateTime(
        _hastodt(datetime.datetime(2005, 3, 1))
    ).dt == datetime.datetime(2005, 3, 1)

    with pytest.raises(ValueError):
        _DateTime(3.0)

def mkdt(*args):
    return datetime.datetime(*args)

def test_datetime_translate_dates():
    s20210301 = _DateTime(20210301) # not a weekend or holidays
    s20210306 = _DateTime(20210306) # weekend (sat)
    s20210528 = _DateTime(20210528) # busday before memday in US
    s20210524 = _DateTime(20210524) # week before memday in US
    s20210530 = _DateTime(20210530) # sun before memday in US
    s20210531 = _DateTime(20210531) # memorial day in US
    s20211125 = _DateTime(20211125) # month before XMas in US
    s20211030 = _DateTime(20211030) # test multiple month skips
    s20211101 = _DateTime(20211101) # to test holiday at beginning of months
    s20211201 = _DateTime(20211201) # test month jump to 2022-01-01
    s20211031 = _DateTime(20211031) # to test holiday at end of months
    s20220101 = _DateTime(20220101) # test other direction of month jump
    s20210101 = _DateTime(20210101) # test year jump to 20220101
    s20221201 = _DateTime(20221201) # test -1 year jump to 20211201
    s20221130 = _DateTime(20221130) # test -1 year jump to 20211130
    s20201130 = _DateTime(20201130) # test 1 year jump to 20211130
    s20050301 = _DateTime(20050301) # test year jumps

    # days
    assert s20210301.translate("days", 0) == mkdt(2021, 3, 1)
    assert s20210301.translate("days", 1) == mkdt(2021, 3, 2)
    assert s20210301.translate("days", -1) == mkdt(2021, 2, 28)
    assert s20210301.translate("days", 5) == mkdt(2021, 3, 6)
    assert s20210301.translate("days", 6) == mkdt(2021, 3, 7)
    assert s20210301.translate("business_days", -1) == mkdt(2021, 2, 26)
    assert s20210301.translate("business_days", 5) == mkdt(2021, 3, 8)

    assert s20210306.translate("days", 1) == mkdt(2021, 3, 7)
    assert s20210306.translate("business_days", 1) == mkdt(2021, 3, 8)
    assert s20210306.translate("business_days", 2) == mkdt(2021, 3, 9)

    assert s20210530.translate("days", 1) == mkdt(2021, 5, 31)
    assert s20210530.translate("days", 1, holidays.US()) == mkdt(2021, 6, 1)

    assert s20210528.translate("days", 1) == mkdt(2021, 5, 29)
    assert s20210528.translate("business_days", 1) == mkdt(2021, 5, 31)
    assert s20210528.translate("business_days", 1, holidays.US()) == mkdt(2021, 6, 1)

    # weeks
    assert s20210301.translate("weeks", 1) == mkdt(2021, 3, 8)
    assert s20210301.translate("weeks", 2) == mkdt(2021, 3, 15)
    assert s20210301.translate("weeks", -1) == mkdt(2021, 2, 22)

    assert s20210306.translate("weeks", 1) == mkdt(2021, 3, 13)

    assert s20210524.translate("weeks", 1, holidays.US()) == mkdt(2021, 6, 1)
    assert s20210306.translate("weeks", 1, None) == mkdt(2021, 3, 13)

    assert s20211125.translate("months", 1, holidays.US()) == mkdt(2021, 12, 26)
    assert s20211125.translate("months", 1, None) == mkdt(2021, 12, 25)

    # make sure month jump into a holiday at end of month and beginning of months
    # works appropriately
    test_holidays = holidays.US().copy()
    test_holidays["2021-12-01"] = "Fake Holiday"
    test_holidays["2021-11-30"] = "Fake Holiday"
    test_holidays["2022-01-01"] = "Fake Holiday" # or is it?!?

    assert s20211101.translate("months", 1, test_holidays) == mkdt(2021, 12, 2)
    assert s20211031.translate("months", 1, test_holidays) == mkdt(2021, 11, 29)
    assert s20211201.translate("months", 1, test_holidays) == mkdt(2022, 1, 2)
    assert s20220101.translate("months", -1, test_holidays) == mkdt(2021, 12, 2)

    assert s20221201.translate("years", -1) == mkdt(2021, 12, 1)
    assert s20221201.translate("years", -1, test_holidays) == mkdt(2021, 12, 2)
    assert s20210101.translate("years", 1) == mkdt(2022, 1, 1)
    assert s20210101.translate("years", 1, test_holidays) == mkdt(2022, 1, 2)
    assert s20221130.translate("years", -1) == mkdt(2021, 11, 30)
    assert s20221130.translate("years", -1, test_holidays) == mkdt(2021, 11, 29)
    assert s20201130.translate("years", 1, test_holidays) == mkdt(2021, 11, 29)

    # make sure if we iterate by months (or years) and pass through a holiday, we don't
    # change our landing date
    assert s20211030.translate("months", 2, test_holidays) == mkdt(2021, 12, 30)
    assert s20211030.translate("months", 1, test_holidays) == mkdt(2021, 11, 29)

    # same as above, but for a weekend
    assert s20050301.translate("years", -20) == mkdt(1985, 3, 1)

    # make sure if we try a month iter into a month that is all holidays we
    # raise an exception rather than iterate infinitely
    begin = mkdt(2021, 1, 1)
    end = mkdt(2021, 1, 31)
    for d in (begin + datetime.timedelta(days=n) for n in range((end-begin).days+1)):
        test_holidays[d.strftime("%Y-%m-%d")] = "Fake Holiday"
    with pytest.raises(ValueError):
        x = s20201130.translate("months", 2, test_holidays)


    def test_datetime_translate_times():
        s20210301 = _DateTime("2021-03-01 12:00:00.000")
        assert s20210301.translate("minutes", 5) == s20210301.dt + rd(minutes=5)
        assert s20210301.translate("minutes", -5) == s20210301.dt - rd(minutes=5)
        assert s20210301.translate("hours", 5) == s20210301.dt + rd(hours=5)
        assert s20210301.translate("hours", -5) == s20210301.dt - rd(hours=5)
        assert s20210301.translate("seconds", 5) == s20210301.dt + rd(seconds=5)
        assert s20210301.translate("seconds", -5) == s20210301.dt - rd(seconds=5)
        assert s20210301.translate("microseconds", 5) == s20210301.dt + rd(microseconds=5)
        assert s20210301.translate("microseconds", -5) == s20210301.dt - rd(microseconds=5)

        test_holidays = holidays.US().copy()
        test_holidays["2021-03-02"] = "Fake Holiday"

        # we shouldn't skip holidays when translating by sub-days
        assert s20210301.translate("hours", 13) == s20210301.dt + rd(hours=13)
        assert s20210301.translate("hours", 13) == datetime.datetime(2021, 3, 2, 1, 0, 0)
