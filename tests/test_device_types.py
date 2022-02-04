import xmatters.xm_objects.device_types
from .conftest import my_vcr


class TestDeviceTypes:

    @my_vcr.use_cassette('test_get_device_types.json')
    def test_get_device_types(self, xm_test):
        dts = xm_test.device_types().get_device_types()
        assert isinstance(dts, xmatters.xm_objects.device_types.DeviceTypes)
