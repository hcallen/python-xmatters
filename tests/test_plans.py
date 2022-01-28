import pytest
from .conftest import my_vcr


@my_vcr.use_cassette('test_get_plans.json')
@pytest.mark.usefixtures('xm_session')
def test_get_plans(xm_session):
    for plan in xm_session.get_plans():
        pass
        for _ in plan.get_forms():
            pass
        for _ in plan.get_constants():
            pass
        for _ in plan.get_endpoints():
            pass
        for _ in plan.get_properties():
            pass
        for _ in plan.get_libraries():
            pass
