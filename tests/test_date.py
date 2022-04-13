import pytest

from datetime_format.__datetime import (
    _int_to_date,
    _string_to_date,
    _check_date,
    _check_month,
)
import datetime


def test_check_month():
    _check_month(2000, 11)
    with pytest.raises(ValueError):
        _check_month(3001, 1)
    with pytest.raises(ValueError):
        _check_month(999, 1)
    with pytest.raises(ValueError):
        _check_month(2000, 0)
    with pytest.raises(ValueError):
        _check_month(2000, 13)


def test_check_date():
    _check_date(2000, 2, 29)
    _check_date(1999, 2, 28)
    _check_date(2000, 4, 30)
    _check_date(2000, 12, 31)

    with pytest.raises(ValueError):
        _check_date(2020, 12, 0)
    with pytest.raises(ValueError):
        _check_date(2020, 2, 30)
    with pytest.raises(ValueError):
        _check_date(2019, 2, 29)
    with pytest.raises(ValueError):
        _check_date(2020, 4, 31)
    with pytest.raises(ValueError):
        _check_date(2020, 5, 32)


def test_int_to_date():
    assert _int_to_date(20050102) == datetime.date(2005, 1, 2)
    assert _int_to_date(200510) == datetime.date(2005, 10, 1)
    with pytest.raises(ValueError):
        _int_to_date(200513)
    with pytest.raises(ValueError):
        _int_to_date(100000)
    with pytest.raises(ValueError):
        _int_to_date(20000230)
    with pytest.raises(ValueError):
        _int_to_date(99991331)


def test_string_to_date():
    assert _string_to_date("20050102") == datetime.date(2005, 1, 2)
    assert _string_to_date("2005-01-02") == datetime.date(2005, 1, 2)
    assert _string_to_date("2005/01/02") == datetime.date(2005, 1, 2)
    assert _string_to_date("01-02-2005") == datetime.date(2005, 1, 2)
    assert _string_to_date("10-01-20") == datetime.date(2020, 10, 1)
    assert _string_to_date("10-01-98") == datetime.date(1998, 10, 1)

    with pytest.raises(ValueError):
        x = _string_to_date("10-01-1")
        print(x)
