import os

import pytest

import xmatters.errors
import xmatters.factories
from tests.conftest import my_vcr
from tests.helpers import assert_attrs_for_data, all_types_in_factory

filename = os.path.basename(__file__).replace('.py', '')


class TestGet:
    @my_vcr.use_cassette('{}_get.json'.format(filename))
    def test_get_audits(self, xm_test):
        audits = xm_test.audits_endpoint().get_audits()
        assert len(audits) > 0
        for audit in audits:
            assert audit.id is not None

    @pytest.mark.skip()
    @my_vcr.use_cassette('{}_get_by_id.json'.format(filename))
    def test_get_by_id(self, xm_test):
        events = xm_test.events_endpoint().get_events(limit=50)
        assert len(events) > 0
        for event in events:
            audits = xm_test.audits_endpoint().get_audits(event_id=event.id)
            assert iter(audits)
            for audit_object in audits:
                assert audit_object.id is not None


class TestParams:
    @my_vcr.use_cassette('{}_params_type.json'.format(filename))
    def test_audit_type(self, xm_test):
        events = xm_test.events_endpoint().get_events(limit=50)
        assert len(events) > 0
        for event in events:
            audits = list(xm_test.audits_endpoint().get_audits(event_id=event.id, audit_type='event_created'))
            assert len(audits) > 0
            for audit_object in audits:
                assert audit_object.type == 'EVENT_CREATED'

    @my_vcr.use_cassette('{}_params_sort_order.json'.format(filename))
    def test_sort_order(self, xm_test):
        events = xm_test.events_endpoint().get_events(limit=50)
        assert len(events) > 0
        for event in events:
            audits_asc = list(xm_test.audits_endpoint().get_audits(event_id=event.id, sort_order='ASCENDING'))
            audits_dsc = list(xm_test.audits_endpoint().get_audits(event_id=event.id, sort_order='DESCENDING'))
            for a_asc, a_dsc in zip(audits_asc, audits_dsc[::-1]):
                assert a_asc.id == a_dsc.id


class TestAccounting:
    @my_vcr.use_cassette('{}_accounting_types.json'.format(filename))
    def test_types(self, xm_test):
        all_types_in_factory(xm_test.audits_endpoint().get_audits(), xmatters.factories.AuditFactory)

    @my_vcr.use_cassette('{}_accounting_attrs.json'.format(filename))
    def test_attrs(self, xm_test):
        assert_attrs_for_data(xm_test.audits_endpoint().get_audits())
