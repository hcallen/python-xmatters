from xmatters.endpoints.common import Pagination
from .conftest import my_vcr


class TestShifts:

    @my_vcr.use_cassette('test_get_shifts.json')
    def test_get_shifts(self, xm_session):
        for group in xm_session.get_groups():
            shifts = group.get_shifts()
            assert isinstance(shifts, Pagination) or isinstance(shifts, list)

    @my_vcr.use_cassette('test_get_shift_members.json')
    def test_get_shift_members(self, xm_session):
        for group in xm_session.get_groups():
            shifts = group.get_shifts()
            for shift in shifts:
                members = shift.get_members()
                assert isinstance(members, list)
