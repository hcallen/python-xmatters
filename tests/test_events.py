from .conftest import my_vcr
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil import tz
from xmatters.errors import NotFoundError


class TestEvents:

    @my_vcr.use_cassette('test_get_events.json')
    def test_get_events(self, xm_test):
        events = xm_test.events().get_events()
        assert iter(events)
        assert len(events) > 0
        for event in events:
            try:
                assert iter(event.get_audit())
                assert iter(event.get_user_delivery_data(at_time=datetime.utcnow().isoformat()))
                assert iter((event.get_annotations()))
                assert iter(event.messages)
                assert isinstance(event.properties, dict)
                assert iter(event.recipients)
                assert iter(event.targeted_recipients)
                assert iter(event.response_options)
            except NotFoundError:
                pass

    @my_vcr.use_cassette('test_get_events_param_from_to.json')
    def test_get_events_param_from_to(self, xm_test):
        start_dt = (datetime.now() - relativedelta(months=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_dt = ((start_dt + relativedelta(months=1)) - timedelta(microseconds=1))
        from_time = start_dt.isoformat()
        to_time = end_dt.isoformat()
        events = xm_test.events().get_events(from_time=from_time, to_time=to_time, sort_order='DESCENDING',
                                             sort_by='START_TIME')
        for event in events:
            assert event.created.isoformat() >= start_dt.astimezone(tz.tzutc()).isoformat()
            assert event.created.isoformat() <= end_dt.astimezone(tz.tzutc()).isoformat()
