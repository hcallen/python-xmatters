from .conftest import my_vcr


class TestPeople:
    @my_vcr.use_cassette('test_people.json')
    def test_people(self, xm_test):
        people = list(xm_test.people().get_people())
        assert iter(people)
        for person in people:
            assert iter(list(person.roles))
            assert iter(list(person.supervisors))
            assert iter(list(person.devices))
