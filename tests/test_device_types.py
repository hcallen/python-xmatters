import xmatters.xm_objects.device_types
import xmatters.factories
from .conftest import my_vcr


class TestGet:

    @my_vcr.use_cassette('test_get_device_types.json')
    def test_get(self, xm_test):
        dts = xm_test.device_types_endpoint().get_device_types()
        assert isinstance(dts, xmatters.xm_objects.device_types.DeviceTypes)


class TestAccounting:

    @my_vcr.use_cassette('test_device_types_accounting.json')
    def test_accounting(self, xm_test):
        devices = list(xm_test.devices_endpoint().get_devices())
        assert len(devices) > 0
        for device in devices:
            assert device.device_type in xmatters.factories.DeviceFactory.factory_objects.keys()
