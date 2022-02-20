import os

from xmatters import utils
from .conftest import my_vcr
from datetime import datetime, timedelta
from dateutil import tz, parser
from xmatters.errors import NotFoundError


filename = os.path.basename(__file__).replace('.py', '')


class TestGet:

    @my_vcr.use_cassette('{}_get.json'.format(filename))
    def test_get_events(self, xm_test):
        events = xm_test.events_endpoint().get_events()
        assert iter(events)
        assert len(events) > 0
        for event in events:
            try:
                assert iter(event.get_audits())
                assert iter(event.get_user_delivery_data(at=datetime.utcnow().isoformat()))
                assert iter((event.get_annotations()))
                assert iter(event.messages)
                assert isinstance(event.properties, dict)
                assert iter(event.recipients)
                assert iter(event.targeted_recipients)
                assert iter(event.response_options)
            except NotFoundError:
                pass


class TestAccounting:

    # @pytest.mark.skip()
    @my_vcr.use_cassette('{}_get.json'.format(filename))
    def test_attrs(self, xm_test):
        for event in xm_test.events_endpoint().get_events():
            for k in event._api_data.keys():
                snake_k = utils.camel_to_snakecase(k)
                assert hasattr(event, snake_k)
            for a in event.get_audits():
                for k in a._api_data.keys():
                    snake_k = utils.camel_to_snakecase(k)
                    assert hasattr(a, snake_k)
            for u in event.get_user_delivery_data(at=datetime.utcnow().isoformat()):
                for k in u._api_data.keys():
                    snake_k = utils.camel_to_snakecase(k)
                    assert hasattr(u, snake_k)
            for a in event.get_annotations():
                for k in a._api_data.keys():
                    snake_k = utils.camel_to_snakecase(k)
                    assert hasattr(a, snake_k)
            for a in event.get_messages():
                for k in a._api_data.keys():
                    snake_k = utils.camel_to_snakecase(k)
                    assert hasattr(a, snake_k)
            for a in event.get_recipients():
                for k in a._api_data.keys():
                    snake_k = utils.camel_to_snakecase(k)
                    assert hasattr(a, snake_k)
            for a in event.get_targeted_recipients():
                for k in a._api_data.keys():
                    snake_k = utils.camel_to_snakecase(k)
                    assert hasattr(a, snake_k)
            for a in event.get_response_options():
                for k in a._api_data.keys():
                    snake_k = utils.camel_to_snakecase(k)
                    assert hasattr(a, snake_k)


class TestParams:

    @my_vcr.use_cassette('{}_test_params_from_to.json'.format(filename))
    def test_from_to(self, xm_test):
        start_dt = datetime.now() - timedelta(days=5)
        end_dt = datetime.now()
        from_time = start_dt.isoformat()
        to_time = end_dt.isoformat()
        events = xm_test.events_endpoint().get_events(from_=from_time, to=to_time, sort_order='DESCENDING',
                                                      sort_by='START_TIME')
        for event in events:
            assert parser.isoparse(event.created).isoformat() >= start_dt.astimezone(tz.tzutc()).isoformat()
            assert parser.isoparse(event.created).isoformat() <= end_dt.astimezone(tz.tzutc()).isoformat()
