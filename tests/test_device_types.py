import os

import xmatters.objects.device_types
import xmatters.factories
from xmatters import utils
from .conftest import my_vcr

filename = os.path.basename(__file__).replace('.py', '')


class TestGet:

    @my_vcr.use_cassette('{}_get.json'.format(filename))
    def test_get(self, xm_test):
        dts = xm_test.device_types_endpoint().get_device_types()
        assert isinstance(dts, xmatters.objects.device_types.DeviceTypes)


class TestAccounting:

    @my_vcr.use_cassette('{}_get.json'.format(filename))
    def test_types(self, xm_test):
        devices = list(xm_test.devices_endpoint().get_devices())
        assert len(devices) > 0
        for device in devices:
            assert device.device_type in xmatters.factories.DeviceFactory._factory_objects.keys()

    @my_vcr.use_cassette('{}_test_get.json'.format(filename))
    def test_attrs(self, xm_test):
        dts = xm_test.device_types_endpoint().get_device_types()
        for k in dts._api_data.keys():
            snake_k = utils.camel_to_snakecase(k)
            assert hasattr(dts, snake_k)
