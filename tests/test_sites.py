from .conftest import my_vcr


class TestSites:

    @my_vcr.use_cassette('test_sites.json')
    def test_sites(self, xm_test):
        sites = list(xm_test.sites_endpoint().get_sites())
        assert iter(sites)
        for site in sites:
            assert site.id is not None
