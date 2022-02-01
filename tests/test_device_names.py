from .conftest import my_vcr


class TestDeviceNames:

    @my_vcr.use_cassette('test_device_names.json')
    def test_device_names(self, xm_test):
        dns = list(xm_test.device_names().get_device_names())
        assert iter(dns)
