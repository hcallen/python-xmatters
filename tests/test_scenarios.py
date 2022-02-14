from .conftest import my_vcr
import xmatters.objects.forms
import xmatters.objects.plans


class TestScenarios:

    @my_vcr.use_cassette('test_scenarios.json')
    def test_scenarios(self, xm_test):
        scenarios = xm_test.scenarios_endpoint().get_scenarios()
        assert iter(scenarios)
        for scenario in scenarios:
            assert scenario.id is not None
            assert isinstance(scenario.properties, dict)
            assert isinstance(scenario.properties_translations, dict)
            assert isinstance(scenario.plan, xmatters.objects.plans.Plan)
            assert isinstance(scenario.form, xmatters.objects.forms.Form)
