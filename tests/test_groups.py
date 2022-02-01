from .conftest import my_vcr


class TestGroups:

    @my_vcr.use_cassette('test_groups.json')
    def test_groups(self, xm_test):
        groups = list(xm_test.groups().get_groups())
        assert iter(groups)
        for group in groups:
            assert iter(list(group.get_supervisors()))
            assert iter(list(group.get_oncall()))
            assert iter(list(group.get_shifts()))
            assert iter(list(group.get_members()))
            assert iter(group.observers)
