from xmatters.endpoints.common import Pagination
from xmatters.endpoints.scenarios import Scenario
from .conftest import my_vcr


class TestScenarios:

    @my_vcr.use_cassette('test_get_scenarios.json')
    def test_get_scenarios(self, xm_session):
        scenarios = xm_session.get_scenarios()
        assert isinstance(scenarios, Pagination) or isinstance(scenarios, list)

    @my_vcr.use_cassette('test_get_scenario_properties.json')
    def test_get_scenario_properties(self, xm_session):
        scenarios = xm_session.get_scenarios()
        for scenario in scenarios:
            assert isinstance(scenario.properties, dict)

    def test_get_scenario_by_id(self, xm_session):
        scenarios = xm_session.get_scenarios()
        for scenario in scenarios:
            s = xm_session.get_scenario_by_id(scenario.id)
            assert isinstance(s, Scenario)
            break
