import os

from xmatters import utils
from .conftest import my_vcr
import xmatters.objects.shifts

fn = os.path.basename(__file__).replace('.py', '')

class TestGet:

    @my_vcr.use_cassette('{}_get.json'.format(fn))
    def test_get(self, xm_test):
        for group in xm_test.groups_endpoint().get_groups():
            oncall = xm_test.oncall_endpoint().get_oncall(groups=group.id)
            for o in oncall:
                shift_occurrence_members = o.members
                assert iter(shift_occurrence_members)
                assert isinstance(o.shift, xmatters.objects.shifts.Shift) or o.shift is None
                for m in shift_occurrence_members:
                    assert m.member.id is not None


class TestAccounting:

    @my_vcr.use_cassette('{}_get.json'.format(fn))
    def test_attrs(self, xm_test):
        for group in xm_test.groups_endpoint().get_groups():
            for oncall in xm_test.oncall_endpoint().get_oncall(groups=group.id):
                for k in oncall._api_data.keys():
                    snake_k = utils.camel_to_snakecase(k)
                    assert hasattr(oncall, snake_k)
                    shift = oncall.get_shift()
                    if shift:
                        for kk in shift._api_data.keys():
                            snake_k = utils.camel_to_snakecase(kk)
                            assert hasattr(shift, snake_k)


