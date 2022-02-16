import os

import pytest
import xmatters.errors
from xmatters.objects.people import Person, UserQuota
from .conftest import my_vcr

fn = os.path.basename(__file__).replace('.py', '')


class TestCreateUpdateDelete:
    @pytest.mark.order(1)
    def test_create(self, xm_sb):
        with pytest.raises(xmatters.errors.NotFoundError):
            xm_sb.people_endpoint().get_person_by_id('mmcbride')
        data = {"targetName": "mmcbride",
                "firstName": "Mary",
                "lastName": "McBride",
                "recipientType": "PERSON",
                "status": "ACTIVE",
                "roles": ["Standard User"]}
        new_person = xm_sb.people_endpoint().create_person(data)
        assert isinstance(new_person, xmatters.objects.people.Person)
        assert new_person.target_name == 'mmcbride'

    @pytest.mark.order(2)
    def test_update(self, xm_sb):
        person = xm_sb.people_endpoint().get_person_by_id('mmcbride')
        data = {"id": person.id,
                "firstName": "John"}
        mod_person = xm_sb.people_endpoint().update_person(data)
        assert isinstance(mod_person, xmatters.objects.people.Person)
        assert mod_person.first_name == 'John'

    @pytest.mark.order(3)
    def test_delete(self, xm_sb):
        person = xm_sb.people_endpoint().get_person_by_id('mmcbride')
        del_person = xm_sb.people_endpoint().delete_person(person.id)
        with pytest.raises(xmatters.errors.NotFoundError):
            xm_sb.people_endpoint().get_person_by_id(del_person.id)


class TestGet:
    @my_vcr.use_cassette('{}_test_get_people.json'.format(fn))
    def test_get_people(self, xm_test):
        people = xm_test.people_endpoint().get_people()
        assert iter(people)
        for person in people:
            assert person.id is not None

    @my_vcr.use_cassette('{}_test_get_roles.json'.format(fn))
    def test_get_roles(self, xm_test):
        people = xm_test.people_endpoint().get_people()
        for person in people:
            roles = person.roles
            assert iter(roles)
            for role in roles:
                assert role.id is not None

    @my_vcr.use_cassette('{}_test_get_devices.json'.format(fn))
    def test_get_devices(self, xm_test):
        people = xm_test.people_endpoint().get_people()
        for person in people:
            devices = person.get_devices()
            assert iter(devices)
            for device in devices:
                assert device.id is not None

    @my_vcr.use_cassette('{}_test_get_groups.json'.format(fn))
    def test_get_groups(self, xm_test):
        for person in xm_test.people_endpoint().get_people():
            groups_memberships = person.get_groups()
            assert iter(groups_memberships)
            for membership in groups_memberships:
                assert membership.member.id is not None

    @my_vcr.use_cassette('{}_test_get_supervisors.json'.format(fn))
    def test_get_supervisors(self, xm_test):
        for person in xm_test.people_endpoint().get_people():
            supervisors = person.get_supervisors()
            assert iter(supervisors)

    @my_vcr.use_cassette('{}_test_get_person_by_id.json'.format(fn))
    def test_get_person_by_id(self, xm_test):
        for person in xm_test.people_endpoint().get_people():
            person_by_id = xm_test.people_endpoint().get_person_by_id(person.id)
            assert isinstance(person_by_id, Person)

    @my_vcr.use_cassette('{}_test_get_quota.json'.format(fn))
    def test_get_quota(self, xm_test):
        quotas = xm_test.people_endpoint().get_license_quotas()
        assert isinstance(quotas, UserQuota)
        assert quotas.full_users is not None


class TestParams:
    @my_vcr.use_cassette('{}_test_properties.json'.format(fn))
    def test_properties(self, settings, xm_test):
        person_property_name = settings.get('person_property_name')
        person_property_value = True
        people = list(
            xm_test.people_endpoint().get_people(property_names=person_property_name,
                                                 property_values=person_property_value))
        assert iter(people)
        assert len(people) > 0
        for person in people:
            prop = person.properties.get(person_property_name)
            assert prop == person_property_value

    @my_vcr.use_cassette('{}_test_groups.json'.format(fn))
    def test_groups(self, settings, xm_test):
        group1_target_name = settings.get('group1_target_name')
        group2_target_name = settings.get('group2_target_name')
        groups = [group1_target_name, group2_target_name]
        people_by_group = list(xm_test.people_endpoint().get_people(groups=groups))
        assert iter(people_by_group)
        assert len(people_by_group) > 0
        for person in people_by_group:
            group_target_names = [mem.group.target_name.upper() for mem in person.get_groups()]
            assert group1_target_name.upper() in group_target_names or group2_target_name.upper() in group_target_names

    @my_vcr.use_cassette('{}_test_devices_exists_false.json'.format(fn))
    def test_devices_exists_false(self, settings, xm_test):
        people = xm_test.people_endpoint().get_people(devices_dot_exists=False)
        assert len(people) > 0
        for person in people:
            count_person_devices = len(person.get_devices())
            assert count_person_devices == 0

    @my_vcr.use_cassette('{}_test_devices_exists_true.json'.format(fn))
    def test_devices_exists_true(self, settings, xm_test):
        params = {'devices.exists': True}
        people = xm_test.people_endpoint().get_people(params)
        assert len(people) > 0
        for person in people:
            assert len(person.get_devices()) > 0
