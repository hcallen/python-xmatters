import os

from xmatters.xm_objects.groups import GroupQuota
from .conftest import my_vcr


class TestGet:

    @my_vcr.use_cassette('{}_test_get_groups.json'.format(os.path.basename(__file__).removesuffix('.py')))
    def test_get_groups(self, xm_test):
        groups = xm_test.groups().get_groups()
        assert iter(groups)
        assert len(groups) > 0
        for group in groups:
            assert group.id is not None
            assert iter(group.get_oncall())
            assert iter(group.get_shifts())
            assert iter(group.get_members())
            assert iter(group.observers)

    @my_vcr.use_cassette('{}_test_get_supervisors.json'.format(os.path.basename(__file__).removesuffix('.py')))
    def test_get_supervisors(self, xm_test):
        groups = xm_test.groups().get_groups(limit=10)
        assert len(groups) > 0
        for group in groups:
            supervisors = group.get_supervisors()
            assert iter(supervisors)
            assert len(supervisors) > 0
            for supervisor in supervisors:
                assert supervisor.id is not None

    def test_get_license_quota(self, xm_test):
        quotas = xm_test.groups().get_license_quotas()
        assert isinstance(quotas, GroupQuota)
