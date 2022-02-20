import os

from xmatters import utils
from .conftest import my_vcr

filename = os.path.basename(__file__).replace('.py', '')


class TestGet:

    @my_vcr.use_cassette('{}_get.json'.format(filename))
    def test_get(self, xm_test):
        dts = xm_test.dynamic_teams_endpoint().get_dynamic_teams()
        assert iter(dts)
        for team in dts:
            assert iter(team.observers)
            assert iter(team.supervisors)
            assert iter(list(team.get_members()))

class TestAccounting:

    @my_vcr.use_cassette('{}_get.json'.format(filename))
    def test_attrs(self, xm_test):
        for team in xm_test.dynamic_teams_endpoint().get_dynamic_teams():
            for k in team._api_data.keys():
                snake_k = utils.camel_to_snakecase(k)
                assert hasattr(team, snake_k)
            for o in team.get_observers():
                for k in o._api_data.keys():
                    snake_k = utils.camel_to_snakecase(k)
                    assert hasattr(o, snake_k)
            for m in team.get_members():
                for k in m._api_data.keys():
                    snake_k = utils.camel_to_snakecase(k)
                    assert hasattr(m, snake_k)

