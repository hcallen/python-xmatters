from .conftest import my_vcr


class TestIncidents:
    @my_vcr.use_cassette('test_incidents.json')
    def test_incidents(self, xm_test):
        incs = xm_test.incidents().get_incidents()
        assert iter(incs)
        for i in incs:
            assert i.id is not None

