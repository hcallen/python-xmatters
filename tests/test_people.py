from xmatters.xm_objects.people import Person
from .conftest import my_vcr


class TestPeople:
    @my_vcr.use_cassette('test_people.json')
    def test_get_people(self, xm_test):
        people = list(xm_test.people().get_people())
        assert iter(people)
        for person in people:
            assert person.id is not None
            assert iter(list(person.roles))
            assert iter(list(person.supervisors))
            assert iter(list(person.get_devices()))
            groups = list(person.get_groups())
            assert iter(groups)

    @my_vcr.use_cassette('test_people.json')
    def test_get_person_by_id(self, xm_test):
        people = list(xm_test.people().get_people())
        for person in people:
            person_by_id = xm_test.people().get_person_by_id(person.id)
            assert isinstance(person_by_id, Person)

    @my_vcr.use_cassette('test_people.json')
    def test_get_people_by_query_first_name(self, xm_test):
        people_by_first_name = list(xm_test.people().get_people_by_query(first_name='David'))
        assert iter(people_by_first_name)
        assert len(people_by_first_name) > 0

    @my_vcr.use_cassette('test_people.json')
    def test_get_people_param_properties(self, settings, xm_test):
        person_property_name = settings.get('person_property_name')
        person_property_value = True
        people = list(
            xm_test.people().get_people(property_names=person_property_name, property_values=person_property_value))
        assert iter(people)
        assert len(people) > 0
        for person in people:
            prop = person.properties.get(person_property_name)
            assert prop == person_property_value

    @my_vcr.use_cassette('test_people.json')
    def test_get_people_param_group(self, settings, xm_test):
        group1_target_name = settings.get('group1_target_name')
        group2_target_name = settings.get('group2_target_name')
        groups = [group1_target_name, group2_target_name]
        people_by_group = list(xm_test.people().get_people(groups=groups))
        assert iter(people_by_group)
        assert len(people_by_group) > 0
        for person in people_by_group:
            group_target_names = [mem.group.target_name.upper() for mem in person.get_groups()]
            assert group1_target_name.upper() in group_target_names or group2_target_name.upper() in group_target_names
