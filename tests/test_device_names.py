import pytest

import xmatters.xm_objects.device_names
from .conftest import my_vcr


class TestDeviceNames:

    @my_vcr.use_cassette('test_get_device_names.json')
    def test_get_device_names(self, xm_test):
        dns = list(xm_test.device_names().get_device_names())
        assert iter(dns)
        for dn in dns:
            assert dn.id is not None

    @pytest.mark.order(1)
    def test_create_device_name(self, xm_sb):
        data = {'deviceType': 'EMAIL',
                'name': 'Another Email Device',
                'description': 'Another Email Device'}
        new_device_name = xm_sb.device_names().create_device_name(data)
        assert isinstance(new_device_name, xmatters.xm_objects.device_names.DeviceName)
        assert new_device_name.name == 'Another Email Device'

    @pytest.mark.order(2)
    def test_modify_device_name(self, xm_sb):
        device_names = xm_sb.device_names().get_device_names()
        to_modify = None
        for device_name in device_names:
            to_modify = device_name
            if to_modify.name == 'Another Email Device':
                break
        data = {'deviceType': 'EMAIL',
                'name': 'Another Email Device Modified',
                'id': to_modify.id}
        mod_device_name = xm_sb.device_names().update_device_name(data)
        assert isinstance(mod_device_name, xmatters.xm_objects.device_names.DeviceName)
        assert mod_device_name.name == 'Another Email Device Modified'

    @pytest.mark.order(3)
    def test_delete_device_name(self, xm_sb):
        device_names = xm_sb.device_names().get_device_names()
        to_delete = None
        for device_name in device_names:
            to_delete = device_name
            if to_delete.name == 'Another Email Device Modified':
                break
        del_device_name = xm_sb.device_names().delete_device_name(to_delete.id)
        assert isinstance(del_device_name, xmatters.xm_objects.device_names.DeviceName)
        device_names = xm_sb.device_names().get_device_names()
        for device_name in device_names:
            assert device_name.id != to_delete.id

