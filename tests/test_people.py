import pytest
import xmatters.errors
from xmatters.xm_objects.people import Person
from .conftest import my_vcr


class TestCreateUpdateDelete:
    @pytest.mark.order(1)
    def test_create(self, xm_sb):
        with pytest.raises(xmatters.errors.NotFoundError):
            xm_sb.people().get_person_by_id('mmcbride')
        data = {"targetName": "mmcbride",
                "firstName": "Mary",
                "lastName": "McBride",
                "recipientType": "PERSON",
                "status": "ACTIVE",
                "roles": ["Standard User"]}
        new_person = xm_sb.people().create_person(data)
        assert isinstance(new_person, xmatters.xm_objects.people.Person)
        assert new_person.target_name == 'mmcbride'

    @pytest.mark.order(2)
    def test_update(self, xm_sb):
        person = xm_sb.people().get_person_by_id('mmcbride')
        data = {"id": person.id,
                "firstName": "John"}
        mod_person = xm_sb.people().update_person(data)
        assert isinstance(mod_person, xmatters.xm_objects.people.Person)
        assert mod_person.first_name == 'John'

    @pytest.mark.order(3)
    def test_delete(self, xm_sb):
        person = xm_sb.people().get_person_by_id('mmcbride')
        del_person = xm_sb.people().delete_person(person.id)
        with pytest.raises(xmatters.errors.NotFoundError):
            xm_sb.people().get_person_by_id(del_person.id)


class TestGet:
    @my_vcr.use_cassette('people_test_get.json')
    def test_get(self, xm_test):
        people = xm_test.people().get_people()
        assert iter(people)
        for person in people:
            assert person.id is not None

    @my_vcr.use_cassette('people_test_get_roles.json')
    def test_roles(self, xm_test):
        people = xm_test.people().get_people()
        for person in people:
            roles = person.roles
            assert iter(roles)
            for role in roles:
                assert role.id is not None

    @my_vcr.use_cassette('people_test_get_devices.json')
    def test_get_devices(self, xm_test):
        people = xm_test.people().get_people()
        for person in people:
            devices = person.get_devices()
            assert iter(devices)
            for device in devices:
                assert device.id is not None

    @my_vcr.use_cassette('people_test_get_groups.json')
    def test_get_groups(self, xm_test):
        for person in xm_test.people().get_people():
            groups_memberships = person.get_groups()
            assert iter(groups_memberships)
            for membership in groups_memberships:
                assert membership.member.id is not None

    @my_vcr.use_cassette('people_test_get_supervisors.json')
    def test_get_supervisors(self, xm_test):
        for person in xm_test.people().get_people():
            supervisors = person.get_supervisors()
            assert iter(supervisors)

    @my_vcr.use_cassette('test_get_person_by_id.json')
    def test_get_by_id(self, xm_test):
        for person in xm_test.people().get_people():
            person_by_id = xm_test.people().get_person_by_id(person.id)
            assert isinstance(person_by_id, Person)

    @my_vcr.use_cassette('test_get_people_by_query_first_name.json')
    def test_get_by_query(self, xm_test):
        people_by_first_name = list(xm_test.people().get_people_by_query(first_name='David'))
        assert iter(people_by_first_name)
        assert len(people_by_first_name) > 0

    @my_vcr.use_cassette('people_test_get_pagination.json')
    def test_get_pagination(self, xm_test):
        people = xm_test.people().get_people()
        total = people.total
        i = 0
        for _ in people:
            i+= 1
        assert i == total


class TestParams:
    @my_vcr.use_cassette('test_get_people_param_properties.json')
    def test_properties(self, settings, xm_test):
        person_property_name = settings.get('person_property_name')
        person_property_value = True
        people = list(
            xm_test.people().get_people(property_names=person_property_name, property_values=person_property_value))
        assert iter(people)
        assert len(people) > 0
        for person in people:
            prop = person.properties.get(person_property_name)
            assert prop == person_property_value

    @my_vcr.use_cassette('test_get_people_param_group.json')
    def test_groups(self, settings, xm_test):
        group1_target_name = settings.get('group1_target_name')
        group2_target_name = settings.get('group2_target_name')
        groups = [group1_target_name, group2_target_name]
        people_by_group = list(xm_test.people().get_people(groups=groups))
        assert iter(people_by_group)
        assert len(people_by_group) > 0
        for person in people_by_group:
            group_target_names = [mem.group.target_name.upper() for mem in person.get_groups()]
            assert group1_target_name.upper() in group_target_names or group2_target_name.upper() in group_target_names

    @my_vcr.use_cassette('test_get_people_param_limit.json')
    def test_limit(self, settings, xm_test):
        people_limit = xm_test.people().get_people(limit=10)
        people_no_limit = list(list(xm_test.people().get_people())[:10])
        assert len(people_limit) == 10
        assert len(people_no_limit) == 10
        for p1, p2 in zip(people_no_limit, people_limit):
            assert p1.id == p2.id
