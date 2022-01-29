from tests.conftest import my_vcr
from xmatters.endpoints.common import Pagination


class TestSubscriptions:

    @my_vcr.use_cassette('test_get_subscriptions.json')
    def test_get_subscriptions(self, xm_session):
        subs = xm_session.get_subscriptions()
        assert isinstance(subs, Pagination) or isinstance(subs, list)

    @my_vcr.use_cassette('test_subscription_pagination.json')
    def test_subscription_pagination(self, xm_session):
        subs = xm_session.get_subscriptions()
        for sub in subs:
            assert sub.id is not None