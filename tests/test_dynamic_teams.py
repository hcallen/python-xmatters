from .conftest import my_vcr


class TestDynamicTeams:

    @my_vcr.use_cassette('test_dynamic_teams.json')
    def test_dynamic_teams(self, xm):
        dts = list(xm.dynamic_teams.get_dynamic_teams())
        assert iter(dts)
        for team in dts:
            assert iter(team.observers)
            assert iter(team.supervisors)
            assert iter(list(team.get_members()))