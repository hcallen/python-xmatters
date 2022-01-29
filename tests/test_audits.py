from tests.conftest import my_vcr

class TestAudits:

    @my_vcr.use_cassette('test_audits.json')
    def test_audits(self, xm):
        events = list(xm.get_events())
        for event in events:
            assert iter(list(xm.get_audit(event_id=event.id)))
