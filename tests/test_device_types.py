from xmatters.xm_objects.device_types import DeviceTypes
from .conftest import my_vcr


class TestDeviceTypes:

    @my_vcr.use_cassette('test_device_types.json')
    def test_device_types(self, xm):
        dts = xm.device_types().get_device_types()
        assert isinstance(dts, DeviceTypes)
