import pytest

import xmatters.errors as err
from tests.conftest import my_vcr
from xmatters.xm_objects.devices import EmailDevice, Device


class TestDevices:
    @my_vcr.use_cassette('test_get_devices.json')
    def test_get_devices(self, xm_test):
        devices = list(xm_test.devices().get_devices())
        assert len(devices) > 0
        for device in devices:
            assert device.id is not None
            assert iter(list(device.timeframes))

    @my_vcr.use_cassette('test_get_device_by_id.json')
    def test_get_device_by_id(self, xm_test):
        devices = list(xm_test.devices().get_devices())
        assert len(devices) > 0
        for device in devices:
            device_by_id = xm_test.devices().get_device_by_id(device.id)
            assert device.id is not None
            assert isinstance(device_by_id, Device)

    @my_vcr.use_cassette('test_get_devices_param_status.json')
    def test_get_devices_param_status(self, xm_test):
        devices = list(xm_test.devices().get_devices(device_status='INACTIVE'))
        assert len(devices) > 0
        for device in devices:
            assert device.status == 'INACTIVE'

    @my_vcr.use_cassette('test_get_devices_param_type.json')
    def test_get_devices_param_type(self, xm_test):
        devices = list(xm_test.devices().get_devices(device_type='EMAIL'))
        assert len(devices) > 0
        for device in devices:
            assert device.device_type == 'EMAIL'

    @my_vcr.use_cassette('test_get_devices_param_name.json')
    def test_get_devices_param_name(self, xm_test):
        # TODO: Test limitations with params w/ pagination objects; param ordering issue?
        devices = list(xm_test.devices().get_devices(device_names=['Home Email', 'Work Email']))
        assert len(devices) > 0
        for device in devices:
            assert device.name in ('Work Email', 'Home Email')

    @my_vcr.use_cassette('test_get_devices_param_phone_format.json')
    def test_get_devices_param_phone_format(self, xm_test):
        devices = list(xm_test.devices().get_devices(device_type='VOICE', phone_number_format='COUNTRY_CODE'))
        assert len(devices) > 0
        for device in devices:
            assert ' ' in device.phone_number

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
