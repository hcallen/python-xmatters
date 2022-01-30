from .conftest import my_vcr


class TestSites:

    @my_vcr.use_cassette('test_sites.json')
    def test_sites(self, xm):
        sites = list(xm.sites().get_sites())
        assert iter(sites)
