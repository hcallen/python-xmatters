from .conftest import my_vcr


class TestOnCallSummary:

    @my_vcr.use_cassette('test_oncall_summary.json')
    def test_oncall_summary(self, xm):
        for group in xm.groups.get_groups():
            oncall_summ = xm.oncall_summary.get_oncall_summary(group.id)
            assert iter(oncall_summ)