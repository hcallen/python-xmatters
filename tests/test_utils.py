from datetime import datetime

from xmatters.utils import TimeAttribute


class TestUtils:
    def test_timeattribute(self):
        time_attr = TimeAttribute('2021-05-06T19:53:27.387Z')
        assert isinstance(time_attr, str)
        assert isinstance(time_attr.datetime(), datetime)
        assert isinstance(time_attr.local_datetime(), datetime)
