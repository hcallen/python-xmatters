from xmatters.endpoints.common import Pagination
from xmatters.endpoints.incidents import Incident
from .conftest import my_vcr


class TestIncidents:
    @my_vcr.use_cassette('test_get_incidents.json')
    def test_get_incidents(self, xm_session):
        incs = xm_session.get_incidents()
        assert isinstance(incs, Pagination) or isinstance(incs, list)
        for inc in incs:
            assert isinstance(inc, Incident)
