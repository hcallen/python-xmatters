from .conftest import my_vcr
import xmatters.errors as err


class TestEvents:

    @my_vcr.use_cassette('test_events.json')
    def test_events(self, xm_test):
        events = list(xm_test.events().get_events())
        assert iter(events)
        assert len(events) > 0
        for event in events:
            try:
                assert iter(list(event.get_audit()))
                at_param = event.created.datetime().replace(minute=59, second=59).isoformat()
                assert iter(list(event.get_user_delivery_data(at=at_param)))
                assert iter(list(event.get_annotations()))
                assert iter(list(event.messages))
                assert isinstance(event.properties, dict)
                assert iter(list(event.recipients))
                assert iter(list(event.targeted_recipients))
                assert iter(event.response_options)
            except err.NotFoundError:
                # skip audits not found due to not being on the cassette
                pass
