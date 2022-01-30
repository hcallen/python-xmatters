from .conftest import my_vcr


class TestConferenceBridges:

    @my_vcr.use_cassette('test_conference_bridges.json')
    def test_conference_bridges(self, xm):
        bridges = list(xm.conference_bridges.get_conference_bridges())
        assert iter(bridges)
