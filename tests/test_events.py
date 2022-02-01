from .conftest import my_vcr
import xmatters.errors as err


class TestEvents:

    @my_vcr.use_cassette('test_events.json')
    def test_events(self, xm_test):
        events = list(xm_test.events().get_events())
        assert iter(events)
        for event in events:
            try:
                assert iter(list(event.get_audit()))
            except err.NotFoundError:
                # skip audits not found due to not being on the cassette
                pass
            assert iter(list(event.annotations))
            assert iter(list(event.messages))
            assert isinstance(event.properties, dict)
            assert iter(list(event.recipients))
            assert iter(event.response_options)
