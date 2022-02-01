from .conftest import my_vcr


class TestOnCall:

    @my_vcr.use_cassette('test_oncall.json')
    def test_oncall(self, xm_test):
        for group in xm_test.groups().get_groups():
            oncall = xm_test.oncall().get_oncall(group.id)
            for o in oncall:
                assert iter(list(o.members))
