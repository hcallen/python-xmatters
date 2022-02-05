from .conftest import my_vcr


class TestServices:

    @my_vcr.use_cassette('test_services.json')
    def test_services(self, xm_test):
        services = xm_test.services().get_services()
        assert iter(services)
        for service in services:
            assert service.id is not None
