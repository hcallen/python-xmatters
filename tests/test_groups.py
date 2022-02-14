import os

from xmatters.xm_objects.groups import GroupQuota
from .conftest import my_vcr

fn = os.path.basename(__file__).replace('.py', '')


class TestGet:

    @my_vcr.use_cassette('{}_test_get_groups.json'.format(fn))
    def test_get_groups(self, xm_test):
        groups = xm_test.groups_endpoint().get_groups()
        assert iter(groups)
        assert len(groups) > 0
        for group in groups:
            assert group.id is not None
            assert iter(group.get_oncall())
            assert iter(group.get_shifts())
            assert iter(group.get_members())
            assert iter(group.observers)

    @my_vcr.use_cassette('{}_test_get_oncall.json'.format(fn))
    def test_get_oncall(self, xm_test):
        groups = xm_test.groups_endpoint().get_groups(limit=10)
        assert iter(groups)
        assert len(groups) > 0
        for group in groups:
            oncalls =  group.get_oncall()
            assert iter(oncalls)
            for oncall in oncalls:
                assert oncall.group.id is not None

    @my_vcr.use_cassette('{}_test_get_supervisors.json'.format(fn))
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
