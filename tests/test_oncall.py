from .conftest import my_vcr


class TestOnCall:

    @my_vcr.use_cassette('test_oncall.json')
    def test_oncall(self, xm):
        for group in xm.groups.get_groups():
            oncall = xm.oncall.get_oncall(group.id)
            for o in oncall:
                assert iter(list(o.members))