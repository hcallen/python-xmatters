from tests.conftest import my_vcr
import xmatters.errors
import xmatters.factories


class TestGet:
    @my_vcr.use_cassette('test_get_audit.json')
    def test_get(self, xm_test):
        audits = xm_test.audits().get_audit()
        assert len(audits) > 0
        for audit in audits:
            assert audit.id is not None

    @my_vcr.use_cassette('test_get_audit_by_event_id.json')
    def test_get_by_id(self, xm_test, events_last_month):
        assert len(events_last_month) > 0
        for event in events_last_month:
            audits = xm_test.audits().get_audit(event_id=event.id)
            assert iter(audits)
            for audit_object in audits:
                assert audit_object.id is not None


class TestParams:
    @my_vcr.use_cassette('test_get_audit_param_type.json')
    def test_audit_type(self, xm_test, events_last_month):
        assert len(events_last_month) > 0
        for event in events_last_month:
            audits = list(xm_test.audits().get_audit(event_id=event.id, audit_type='event_created'))
            assert len(audits) > 0
            for audit_object in audits:
                assert audit_object.type == 'EVENT_CREATED'

    @my_vcr.use_cassette('test_get_audit_param_sort_order.json')
    def test_sort_order(self, xm_test, events_last_month):
        assert len(events_last_month) > 0
        for event in events_last_month:
            audits_asc = list(xm_test.audits().get_audit(event_id=event.id, sort_order='ASCENDING'))
            audits_dsc = list(xm_test.audits().get_audit(event_id=event.id, sort_order='DESCENDING'))
            for a_asc, a_dsc in zip(audits_asc, audits_dsc[::-1]):
                assert a_asc.id == a_dsc.id


class TestAccounting:
    @my_vcr.use_cassette('test_audit_types_accounting.json')
    def test_accounting(self, xm_test, events_last_month):
        assert len(events_last_month) > 0
        for event in events_last_month:
            audits = list(xm_test.audits().get_audit(event_id=event.id))
            for audit in audits:
                assert audit.type in xmatters.factories.AuditFactory.factory_objects.keys()
