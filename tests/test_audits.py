from tests.conftest import my_vcr


class TestAudits:

    @my_vcr.use_cassette('test_audits.json')
    def test_audits(self, xm):
        events = list(xm.events().get_events())
        for event in events:
            audits = list(xm.audits().get_audit(event_id=event.id))
            assert iter(audits)
            for audit_object in audits:
                assert audit_object.id is not None
