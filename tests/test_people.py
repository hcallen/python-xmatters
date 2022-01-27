import pytest
from .conftest import my_vcr


@my_vcr.use_cassette('test_get_people')
@pytest.mark.usefixtures('xm_session')
def test_get_people(xm_session):
    for person in xm_session.get_people():
        assert person.id is not None
        assert isinstance(person.properties, dict)


