from xmatters.xm_objects.people import Person
from .conftest import my_vcr
import xmatters.errors as err


class TestPlans:
    @my_vcr.use_cassette('test_plans.json')
    def test_plans(self, xm_test):
        plans = list(xm_test.plans().get_plans())
        assert iter(list(plans))
        assert len(plans) > 0
        for plan in plans:
            try:
                assert iter(list(plan.get_forms()))
                assert iter(list(plan.get_constants()))
                assert iter(list(plan.get_integrations()))
                assert iter(list(plan.get_properties()))
                assert iter(list(plan.get_shared_libraries()))
                assert iter(list(plan.get_endpoints()))
                assert iter(list(plan.get_subscription_forms()))
                creator = plan.creator
                assert isinstance(creator, Person) or creator is None
            except err.ForbiddenError:
                # skip plans that account doesn't have access to
                pass
