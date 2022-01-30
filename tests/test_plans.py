from xmatters.xm_objects.people import Person
from .conftest import my_vcr


class TestPlans:
    @my_vcr.use_cassette('test_plans.json')
    def test_plans(self, xm):
        plans = list(xm.plans().get_plans())
        assert iter(list(plans))
        for plan in plans:
            assert iter(list(plan.get_forms()))
            assert iter(list(plan.get_constants()))
            assert iter(list(plan.get_integrations()))
            assert iter(list(plan.get_properties()))
            assert iter(list(plan.get_libraries()))
            assert iter(list(plan.get_endpoints()))
            assert iter(list(plan.get_subscription_forms()))
            creator = plan.creator
            assert isinstance(creator, Person) or creator is None
