import pytest
from betamax import Betamax

from xmatters.common import Pagination, Recipient


class TestxMattersSession:

    def test_get_devices(self, xm_session):
        with Betamax(xm_session.con.session) as vcr:
            vcr.use_cassette('get_devices')
            devices = xm_session.get_devices()
        assert isinstance(devices, Pagination)
        assert devices.total is not None

    def test_get_people(self, xm_session):
        with Betamax(xm_session.con.session) as vcr:
            vcr.use_cassette('get_people')
            people = xm_session.get_people()
        assert isinstance(people, Pagination)
        assert people.total is not None

    @pytest.mark.skip()
    def test_get_device_by_id(self, xm_session, settings):
        with Betamax(xm_session.con.session) as vcr:
            vcr.use_cassette('get_device_by_id')
            device = xm_session.get_device_by_id(settings['device_id'])
        assert isinstance(device, Recipient)
        assert device.id is not None
