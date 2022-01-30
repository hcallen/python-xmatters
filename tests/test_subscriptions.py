from tests.conftest import my_vcr


class TestSubscriptions:

    @my_vcr.use_cassette('test_subscriptions.json')
    def test_subscriptions(self, xm):
        subs = list(xm.subscriptions().get_subscriptions())
        assert iter(subs)
        for sub in subs:
            assert iter(list(sub.get_subscribers()))
