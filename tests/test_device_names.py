import os

import pytest

import xmatters.objects.device_names
from xmatters import utils
from .conftest import my_vcr

filename = os.path.basename(__file__).replace('.py', '')


class TestCreateUpdateDelete:
    @pytest.mark.order(1)
    def test_create(self, xm_sb):
        data = {'deviceType': 'EMAIL',
                'name': 'Another Email Device',
                'description': 'Another Email Device'}
        new_device_name = xm_sb.device_names_endpoint().create_device_name(data)
        assert isinstance(new_device_name, xmatters.objects.device_names.DeviceName)
        assert new_device_name.name == 'Another Email Device'

    @pytest.mark.order(2)
    def test_update(self, xm_sb):
        device_names = xm_sb.device_names_endpoint().get_device_names()
        to_modify = None
        for device_name in device_names:
            to_modify = device_name
            if to_modify.name == 'Another Email Device':
                break
        data = {'deviceType': 'EMAIL',
                'name': 'Another Email Device Modified',
                'id': to_modify.id}
        mod_device_name = xm_sb.device_names_endpoint().update_device_name(data)
        assert isinstance(mod_device_name, xmatters.objects.device_names.DeviceName)
        assert mod_device_name.name == 'Another Email Device Modified'

    @pytest.mark.order(3)
    def test_delete(self, xm_sb):
        device_names = xm_sb.device_names_endpoint().get_device_names()
        to_delete = None
        for device_name in device_names:
            to_delete = device_name
            if to_delete.name == 'Another Email Device Modified':
                break
        del_device_name = xm_sb.device_names_endpoint().delete_device_name(to_delete.id)
        assert isinstance(del_device_name, xmatters.objects.device_names.DeviceName)
        device_names = xm_sb.device_names_endpoint().get_device_names()
        for device_name in device_names:
            assert device_name.id != to_delete.id


class TestGet:

    @my_vcr.use_cassette('{}_get.json'.format(filename))
    def test_get(self, xm_test):
        dns = xm_test.device_names_endpoint().get_device_names()
        assert iter(dns)
        for dn in dns:
            assert dn.id is not None


class TestAccounting:

    @my_vcr.use_cassette('{}_get.json'.format(filename))
    def test_attrs(self, xm_test):
        dns = xm_test.device_names_endpoint().get_device_names()
        for dn in dns:
            for k in dn._api_data.keys():
                snake_k = utils.camel_to_snakecase(k)
                assert hasattr(dn, snake_k)
