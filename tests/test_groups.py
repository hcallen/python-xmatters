import os

from xmatters import utils
from xmatters.objects.groups import GroupQuota
from .conftest import my_vcr

fn = os.path.basename(__file__).replace('.py', '')


class TestGet:

    @my_vcr.use_cassette('{}_get.json'.format(fn))
    def test_get_groups(self, xm_test):
        groups = xm_test.groups_endpoint().get_groups()
        assert iter(groups)
        assert len(groups) > 0
        for group in groups:
            assert group.id is not None
            assert iter(group.get_oncall())
            assert iter(group.get_shifts())
            assert iter(group.get_members())
            assert iter(group.get_observers())

    @my_vcr.use_cassette('{}_get_oncall.json'.format(fn))
    def test_get_oncall(self, xm_test):
        groups = xm_test.groups_endpoint().get_groups(limit=10)
        assert iter(groups)
        assert len(groups) > 0
        for group in groups:
            oncalls =  group.get_oncall()
            assert iter(oncalls)
            for oncall in oncalls:
                assert oncall.group.id is not None

    @my_vcr.use_cassette('{}_get_supervisors.json'.format(fn))
    def test_get_supervisors(self, xm_test):
        groups = xm_test.groups_endpoint().get_groups(limit=10)
        assert len(groups) > 0
        for group in groups:
            supervisors = group.get_supervisors()
            assert iter(supervisors)
            assert len(supervisors) > 0
            for supervisor in supervisors:
                assert supervisor.id is not None

    def test_get_license_quota(self, xm_test):
        quotas = xm_test.groups_endpoint().get_license_quotas()
        assert isinstance(quotas, GroupQuota)

class TestAccounting:

    @my_vcr.use_cassette('{}_get.json'.format(fn))
    def test_attrs(self, xm_test):
        for group in xm_test.groups_endpoint().get_groups():
            for k in group._api_data.keys():
                snake_k = utils.camel_to_snakecase(k)
                assert hasattr(group, snake_k)
            for i in group.get_observers():
                for k in i._api_data.keys():
                    snake_k = utils.camel_to_snakecase(k)
                    assert hasattr(i, snake_k)
            for i in group.get_supervisors():
                for k in i._api_data.keys():
                    snake_k = utils.camel_to_snakecase(k)
                    assert hasattr(i, snake_k)
            for i in group.get_oncall():
                for k in i._api_data.keys():
                    snake_k = utils.camel_to_snakecase(k)
                    assert hasattr(i, snake_k)
            for i in group.get_shifts():
                for k in i._api_data.keys():
                    snake_k = utils.camel_to_snakecase(k)
                    assert hasattr(i, snake_k)
