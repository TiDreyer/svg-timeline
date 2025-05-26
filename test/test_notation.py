""" test cases for the classes defined in the notation module """
from datetime import datetime

import pytest

from svg_timeline.notation import dt


def test_shorthand():
    # pure dates
    assert dt('1987') == datetime(1987, 1, 1)
    assert dt('1987-09') == datetime(1987, 9, 1)
    assert dt('1987-09-23') == datetime(1987, 9, 23)
    # date + time
    assert dt('1987-09-23T03') == datetime(1987, 9, 23, 3)
    assert dt('1987-09-23T03:23') == datetime(1987, 9, 23, 3, 23)
    assert dt('1987-09-23T03:23:45') == datetime(1987, 9, 23, 3, 23, 45)
    # pure times
    today = datetime.today()
    assert dt('13:43') == datetime(today.year, today.month, today.day, 13, 43)
    assert dt('13:43:52') == datetime(today.year, today.month, today.day, 13, 43, 52)
    with pytest.raises(ValueError):
        dt('asdf')
