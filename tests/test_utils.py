from datetime import datetime

from xmatters.utils.utils import TimeAttribute


def test_timeattribute():
    time_attr = TimeAttribute('2021-05-06T19:53:27.387Z')
    assert isinstance(time_attr, str)
    assert isinstance(time_attr.to_dt(), datetime)
    assert isinstance(time_attr.to_local_dt(), datetime)
