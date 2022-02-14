from xmatters.objects.people import Person
from .conftest import my_vcr
import xmatters.errors as err


class TestPlans:
    @my_vcr.use_cassette('test_plans.json')
    def test_plans(self, xm_test):
        plans = list(xm_test.plans_endpoint().get_plans())
        assert iter(plans)
        assert len(plans) > 0
        for plan in plans:
            try:
                assert iter(plan.get_forms())
                assert iter(plan.get_constants())
                assert iter(plan.get_integrations())
                assert iter(plan.get_properties())
                assert iter(plan.get_shared_libraries())
                assert iter(plan.get_endpoints())
                assert iter(plan.get_subscription_forms())
                creator = plan.creator
                assert isinstance(creator, Person) or creator is None
            except err.ForbiddenError:
                # skip plans that account doesn't have access to
                pass
