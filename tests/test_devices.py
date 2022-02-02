import pytest

import xmatters.errors as err
from tests.conftest import my_vcr
from xmatters.xm_objects.devices import EmailDevice


class TestDevices:
    @my_vcr.use_cassette('test_devices.json')
    def test_devices(self, xm_test):
        devices = list(xm_test.devices().get_devices())
        for device in devices:
            assert device.id is not None
            assert iter(list(device.timeframes))

    @pytest.mark.order(1)
    def test_create_device(self, xm_sb, settings):
        target_name = settings.get('target_name')
        with pytest.raises(err.NotFoundError):
            xm_sb.devices().get_device_by_id('{}|Home Email'.format(target_name))
        person = xm_sb.people().get_person_by_id(target_name)
        data = {'deviceType': 'EMAIL',
                'name': 'Home Email',
                'owner': person.id,
                'privileged': False,
                'emailAddress': 'test@test.com'}
        new_device = xm_sb.devices().create_device(data=data)
        assert isinstance(new_device, EmailDevice)
        assert new_device.email_address == 'test@test.com'

    @pytest.mark.order(2)
    def test_modify_device(self, xm_sb, settings):
        target_name = settings.get('target_name')
        device = xm_sb.devices().get_device_by_id('{}|Home Email'.format(target_name))
        data = {'deviceType': 'EMAIL',
                'id': device.id,
                'privileged': False,
                'emailAddress': 'test2@test.com'}
        mod_device = xm_sb.devices().update_device(data=data)
        assert isinstance(mod_device, EmailDevice)
        assert mod_device.email_address == 'test2@test.com'

    @pytest.mark.order(3)
    def test_delete_device(self, settings, xm_sb):
        target_name = settings.get('target_name')
        device = xm_sb.devices().get_device_by_id('{}|Home Email'.format(target_name))
        deleted_device = xm_sb.devices().delete_device(device.id)
        with pytest.raises(err.NotFoundError):
            xm_sb.devices().get_device_by_id(deleted_device.id)
