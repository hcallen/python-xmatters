import os

from .conftest import my_vcr
from datetime import datetime, timedelta
from dateutil import tz, parser
from xmatters.errors import NotFoundError


class TestEvents:

    @my_vcr.use_cassette('{}_test_get_events.json'.format(os.path.basename(__file__).replace('.py', '')))
    def test_get_events(self, xm_test):
        events = xm_test.events_endpoint().get_events()
        assert iter(events)
        assert len(events) > 0
        for event in events:
            try:
                assert iter(event.get_audit())
                assert iter(event.get_user_delivery_data(at=datetime.utcnow().isoformat()))
                assert iter((event.get_annotations()))
                assert iter(event.messages)
                assert isinstance(event.properties, dict)
                assert iter(event.recipients)
                assert iter(event.targeted_recipients)
                assert iter(event.response_options)
            except NotFoundError:
                pass


class TestParams:

    @my_vcr.use_cassette('{}_test_from_to.json'.format(os.path.basename(__file__).replace('.py', '')))
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
