from .conftest import my_vcr


class TestScenarios:

    @my_vcr.use_cassette('test_scenarios.json')
    def test_scenarios(self, xm_test):
        scenarios = xm_test.scenarios().get_scenarios()
        assert iter(scenarios)
        for scenario in scenarios:
            assert scenario.id is not None
            assert isinstance(scenario.properties, dict)
