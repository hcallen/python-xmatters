from xmatters.endpoints.device_types import DeviceTypes
from .conftest import my_vcr


class TestDeviceTypes:

    @my_vcr.use_cassette('test_device_types.json')
    def test_device_types(self, xm):
        dts = xm.get_device_types()
        assert isinstance(dts, DeviceTypes)