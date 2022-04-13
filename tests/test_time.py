import pytest

from datetime_format.__datetime import (
    _int_to_time,
    _string_to_time,
    _check_time,
)
import datetime


def test_check_time():
    with pytest.raises(ValueError):
        _check_time(25, 0, 0, 0)
    with pytest.raises(ValueError):
        _check_time(-1, 0, 0, 0)
    with pytest.raises(ValueError):
        _check_time(23, 60, 0, 0)
    with pytest.raises(ValueError):
        _check_time(23, -1, 0, 0)
    with pytest.raises(ValueError):
        _check_time(23, 59, 60, 0)
    with pytest.raises(ValueError):
        _check_time(23, 59, -1, 0)
    with pytest.raises(ValueError):
        _check_time(23, 59, 59, 9999999)
    with pytest.raises(ValueError):
        _check_time(23, 59, 59, -1)


def test_int_to_time():
    assert _int_to_time(83803) == datetime.time(8,38,3)
    assert _int_to_time(133803) == datetime.time(13,38,3)
    assert _int_to_time(838) == datetime.time(8,38,0)
    assert _int_to_time(8) == datetime.time(8,0,0)
    with pytest.raises(ValueError):
        _int_to_time(250000)
    with pytest.raises(ValueError):
        _int_to_time(25)
    with pytest.raises(ValueError):
        _int_to_time(2500)
    with pytest.raises(ValueError):
        _int_to_time(-100)

def test_string_to_time():
    assert _string_to_time("08:30:15") == datetime.time(8,30,15)
    assert _string_to_time("14:21:27.13") == datetime.time(14,21,27,130000)
    assert _string_to_time("19:47:38.131010") == datetime.time(19,47,38,131010)
    assert _string_to_time("19:47") == datetime.time(19,47,0)
    assert _string_to_time("8:47") == datetime.time(8,47,0)
    assert _string_to_time("13:15:00.999999") == datetime.time(13,15,0,999999)
    with pytest.raises(ValueError):
        _string_to_time("25:00:00")
    with pytest.raises(ValueError):
        _string_to_time("25:00:00.111.111")
    with pytest.raises(ValueError):
        _string_to_time("25")
    with pytest.raises(ValueError):
        _string_to_time("18/14/27")
    with pytest.raises(ValueError):
        _string_to_time("18:61:10")
    with pytest.raises(ValueError):
        _string_to_time("18:03:61")
    with pytest.raises(ValueError):
        _string_to_time("stringtime_in_germany")
