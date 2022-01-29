from tests.conftest import my_vcr
from xmatters.endpoints.common import Pagination


class TestSubscriptionForms:

    @my_vcr.use_cassette('test_get_subscription_forms.json')
    def test_get_subscription_forms(self, xm_session):
        forms = xm_session.get_subscription_forms()
        assert isinstance(forms, Pagination) or isinstance(forms, list)

    @my_vcr.use_cassette('test_subscription_forms_pagination.json')
    def test_subscription_forms_pagination(self, xm_session):
        forms = xm_session.get_subscription_forms()
        for form in forms:
            assert form.id is not None
            dns = form.target_device_names
            assert isinstance(dns, Pagination) or isinstance(dns, list)
