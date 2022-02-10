import os

from xmatters.xm_objects.groups import GroupQuota
from .conftest import my_vcr


class TestGet:

    @my_vcr.use_cassette('{}TestGet.json'.format(os.path.basename(__file__).removesuffix('.py')))
    def test_get(self, xm_test):
        groups = xm_test.groups().get_groups()
        assert iter(groups)
        for group in groups:
            assert group.id is not None
            assert iter(group.get_supervisors())
            assert iter(group.get_oncall())
            assert iter(group.get_shifts())
            assert iter(group.get_members())
            assert iter(group.observers)

    def test_get_license_quota(self, xm_test):
        quotas = xm_test.groups().get_license_quotas()
        assert isinstance(quotas, GroupQuota)
