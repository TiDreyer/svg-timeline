""" test cases for the classes defined in the notation module """
from datetime import datetime

import pytest

from svg_timeline.notation import dt


def test_shorthand():
    assert dt('1987') == datetime(1987, 1, 1)
    assert dt('1987-09') == datetime(1987, 9, 1)
    assert dt('1987-09-23') == datetime(1987, 9, 23)
    today = datetime.today()
    assert dt('13:43') == datetime(today.year, today.month, today.day, 13, 43)
    assert dt('13:43:52') == datetime(today.year, today.month, today.day, 13, 43, 52)
    with pytest.raises(ValueError):
        dt('asdf')
