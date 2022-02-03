from tests.conftest import my_vcr
import xmatters.errors as err


class TestAudits:

    @my_vcr.use_cassette('test_audits.json')
    def test_get_audit(self, xm_test):
        events = list(xm_test.events().get_events())
        for event in events:
            try:
                audits = list(xm_test.audits().get_audit(event_id=event.id))
                print(event.id)
                assert iter(audits)
                for audit_object in audits:
                    assert audit_object.id is not None
            except err.NotFoundError:
                # skip audits not found due to not being on the cassette
                pass

    @my_vcr.use_cassette('test_audits.json')
    def test_get_audit_param_type(self, xm_test):
        events = list(xm_test.events().get_events())
        for event in events:
            try:
                audits = list(xm_test.audits().get_audit(event_id=event.id, audit_type='event_created'))
                assert len(audits) > 0
                for audit_object in audits:
                    assert audit_object.type == 'EVENT_CREATED'
            except err.NotFoundError:
                # skip audits not found due to not being on the cassette
                pass

    @my_vcr.use_cassette('test_audits.json')
    def test_get_audit_param_sort_order(self, xm_test):
        events = list(xm_test.events().get_events())
        for event in events:
            try:
                audits_asc = list(xm_test.audits().get_audit(event_id=event.id, sort_order='ASCENDING'))
                audits_dsc = list(xm_test.audits().get_audit(event_id=event.id, sort_order='DESCENDING'))
                for a_asc, a_dsc in zip(audits_asc, audits_dsc[::-1]):
                    assert a_asc.id == a_dsc.id
            except err.NotFoundError:
                # skip audits not found due to not being on the cassette
                pass
