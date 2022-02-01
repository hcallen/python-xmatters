from .conftest import my_vcr


class TestScenarios:

    @my_vcr.use_cassette('test_scenarios.json')
    def test_scenarios(self, xm_test):
        scenarios = list(xm_test.scenarios().get_scenarios())
        assert iter(scenarios)
        for scenario in scenarios:
            assert isinstance(scenario.properties, dict)
