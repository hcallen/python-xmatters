from .conftest import my_vcr


class TestEvents:

    @my_vcr.use_cassette('test_events.json')
    def test_events(self, xm_test):
        events = list(xm_test.events().get_events())
        assert iter(events)
        for event in events:
            assert iter(list(event.get_audit()))
            assert iter(list(event.annotations))
            assert iter(list(event.messages))
            assert isinstance(event.properties, dict)
            assert iter(list(event.recipients))
            assert iter(event.response_options)
