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

    def test_create_modify_delete_device(self, settings, xm_sb):
        target_name = settings.get('target_name')
        person = xm_sb.people().get_person_by_id(target_name)
        data = {'deviceType': 'EMAIL',
                'name': 'Home Email',
                'owner': person.id,
                'privileged': False,
                'emailAddress': 'test@test.com'}
        device = xm_sb.devices().create_device(data=data)
        assert isinstance(device, EmailDevice)
        assert device.device_type == 'EMAIL'
        assert device.email_address == 'test@test.com'
        data = {'deviceType': 'EMAIL',
                'id': device.id,
                'privileged': False,
                'emailAddress': 'test2@test.com'}
        device = xm_sb.devices().modify_device(data=data)
        assert isinstance(device, EmailDevice)
        assert device.email_address == 'test2@test.com'
        device = xm_sb.devices().delete_device(device.id)
        with pytest.raises(err.NotFoundError):
            xm_sb.devices().get_device_by_id(device.id)
