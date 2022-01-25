import pytest


class TestxMattersSession:

    def test_get_devices(self, xm_session, pagination_factory):
        pagination_factory(xm_session, 'get_devices')

    @pytest.mark.skip('TODO')
    def test_get_device_by_id(self):
        pass

    def test_get_groups(self, xm_session, pagination_factory):
        pagination_factory(xm_session, 'get_groups')

    @pytest.mark.skip('TODO')
    def test_get_group_by_id(self):
        pass

    def test_get_people(self, xm_session, pagination_factory):
        pagination_factory(xm_session, 'get_people')

    @pytest.mark.skip('TODO')
    def test_get_person_by_id(self):
        pass

    @pytest.mark.skip('TODO')
    def test_get_oncall(self):
        pass

    @pytest.mark.skip('TODO')
    def test_get_oncall_summary(self):
        pass

    def test_get_events(self, xm_session, pagination_factory):
        pagination_factory(xm_session, 'get_events')

    @pytest.mark.skip('TODO')
    def test_get_event_by_id(self):
        pass

    def test_get_temporary_absences(self, xm_session, pagination_factory):
        pagination_factory(xm_session, 'get_temporary_absences')

    @pytest.mark.skip('TODO')
    def test_get_audit(self):
        pass

    def test_get_device_names(self, xm_session, pagination_factory):
        pagination_factory(xm_session, 'get_device_names')

    @pytest.mark.skip('FIX')
    def test_get_device_types(self, xm_session, pagination_factory):
        pagination_factory(xm_session, 'get_device_types')

    def test_get_dynamic_teams(self, xm_session, pagination_factory):
        pagination_factory(xm_session, 'get_dynamic_teams')

    @pytest.mark.skip('TODO')
    def test_get_dynamic_team_by_id(self):
        pass

    @pytest.mark.skip('FIX')
    def test_get_conference_bridges(self, xm_session, pagination_factory):
        pagination_factory(xm_session, 'get_conference_bridges')

    @pytest.mark.skip('TODO')
    def test_conference_bridge_by_id(self):
        pass

    def test_get_forms(self, xm_session, pagination_factory):
        pagination_factory(xm_session, 'get_forms')

    @pytest.mark.skip('TODO')
    def test_get_import_jobs(self):
        pass
