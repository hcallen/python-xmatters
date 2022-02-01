from .conftest import my_vcr


class TestShifts:

    @my_vcr.use_cassette('test_shifts.json')
    def test_get_shifts(self, xm_test):
        for group in xm_test.groups().get_groups():
            shifts = list(group.get_shifts())
            assert iter(list(shifts))
            for shift in shifts:
                assert iter(list(shift.get_members()))

