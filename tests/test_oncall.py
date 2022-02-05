from .conftest import my_vcr
import xmatters.xm_objects.shifts

class TestOnCall:

    @my_vcr.use_cassette('test_oncall.json')
    def test_oncall(self, xm_test):
        for group in xm_test.groups().get_groups():
            oncall = xm_test.oncall().get_oncall(group.id)
            for o in oncall:
                shift_occurrence_members = o.members
                assert iter(shift_occurrence_members)
                assert isinstance(o.shift, xmatters.xm_objects.shifts.Shift) or o.shift is None
                for m in shift_occurrence_members:
                    assert m.member.id is not None
