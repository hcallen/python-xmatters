from .conftest import my_vcr


class TestIncidents:
    @my_vcr.use_cassette('test_incidents.json')
    def test_incidents(self, xm_test):
        assert iter(list(xm_test.incidents().get_incidents()))
