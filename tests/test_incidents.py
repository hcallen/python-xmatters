import os

from xmatters import utils
from .conftest import my_vcr

fn = os.path.basename(__file__).replace('.py', '')

class TestGet:

    @my_vcr.use_cassette('{}_get.json'.format(fn))
    def test_get(self, xm_test):
        incs = xm_test.incidents_endpoint().get_incidents()
        assert iter(incs)
        for i in incs:
            assert i.id is not None


class TestAccounting:

    @my_vcr.use_cassette('{}_get.json'.format(fn))
    def test_attrs(self, xm_test):
        for inc in xm_test.incidents_endpoint().get_incidents():
            for k in inc._api_data.keys():
                snake_k = utils.camel_to_snakecase(k)
                assert hasattr(inc, snake_k)

