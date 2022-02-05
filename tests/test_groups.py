from .conftest import my_vcr


class TestGroups:

    @my_vcr.use_cassette('test_groups.json')
    def test_groups(self, xm_test):
        groups = xm_test.groups().get_groups()
        assert iter(groups)
        for group in groups:
            assert group.id is not None
            assert iter(group.get_supervisors())
            assert iter(group.get_oncall())
            assert iter(group.get_shifts())
            assert iter(group.get_members())
            assert iter(group.observers)
