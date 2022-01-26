import pytest
from .conftest import my_vcr
from xmatters.common import Pagination


@my_vcr.use_cassette('test_people')
@pytest.mark.usefixtures('xm_session')
def test_get_people(xm_session):
    for person in xm_session.get_people():
        assert person.id is not None
        assert isinstance(person.properties, dict)
        assert isinstance(person.supervisors, Pagination) or isinstance(person.supervisors, list)

