from .conftest import my_vcr


class TestIncidents:
    @my_vcr.use_cassette('test_incidents.json')
    def test_incidents(self, xm):
        assert iter(list(xm.get_incidents()))
