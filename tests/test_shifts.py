from .conftest import my_vcr


class TestShifts:

    @my_vcr.use_cassette('test_shifts.json')
    def test_get_shifts(self, xm_test):
        for group in xm_test.groups_endpoint().get_groups():
            shifts = group.get_shifts()
            assert iter(shifts)
            for shift in shifts:
                assert shift.id is not None
                assert iter(shift.get_members())

