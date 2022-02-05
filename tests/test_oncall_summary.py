from .conftest import my_vcr


class TestOnCallSummary:

    @my_vcr.use_cassette('test_oncall_summary.json')
    def test_oncall_summary(self, xm_test):
        for group in xm_test.groups().get_groups():
            oncall_summ = xm_test.oncall_summary().get_oncall_summary(group.id)
            assert iter(oncall_summ)
            for o in oncall_summ:
                assert o.group.id is not None
