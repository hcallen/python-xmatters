import os

from xmatters import utils
from .conftest import my_vcr

fn = os.path.basename(__file__).replace('.py', '')


class TestGet:

    @my_vcr.use_cassette('{}_get.json'.format(fn))
    def test_import_jobs(self, xm_test):
        jobs = xm_test.imports_endpoint().get_import_jobs()
        assert iter(jobs)
        for job in jobs:
            assert iter(job.get_messages())


class TestAccounting:

    @my_vcr.use_cassette('{}_get.json'.format(fn))
    def test_attrs(self, xm_test):
        for job in xm_test.imports_endpoint().get_import_jobs():
            for k in job._api_data.keys():
                snake_k = utils.camel_to_snakecase(k)
                assert hasattr(job, snake_k)
            for i in job.get_messages():
                for k in i._api_data.keys():
                    snake_k = utils.camel_to_snakecase(k)
                    assert hasattr(i, snake_k)
