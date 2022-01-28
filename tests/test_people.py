import pytest

from xmatters.common import Pagination
from xmatters.people import Person
from .conftest import my_vcr


class TestPeople:
    @my_vcr.use_cassette('test_get_people.json')
    def test_get_people(self, xm_session):
        for person in xm_session.get_people():
            assert person.id is not None
            assert isinstance(person, Person)

    @my_vcr.use_cassette('test_get_people_devices.json')
    def test_get_people_devices(self, xm_session):
        for person in xm_session.get_people():
            assert isinstance(person.get_devices(), list)

    @my_vcr.use_cassette('test_get_people_roles.json')
    def test_get_people_roles(self, xm_session):
        for person in xm_session.get_people():
            roles = person.roles
            assert isinstance(roles, Pagination) or isinstance(roles, list)

    @my_vcr.use_cassette('test_get_people_supervisors.json')
    def test_get_people_supervisors(self, xm_session):
        for person in xm_session.get_people():
            supervisors = person.supervisors
            assert isinstance(supervisors, Pagination) or isinstance(supervisors, list)
