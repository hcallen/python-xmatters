import os

import xmatters.factories
from xmatters import utils
from .conftest import my_vcr

fn = os.path.basename(__file__).replace('.py', '')


class TestGet:

    @my_vcr.use_cassette('{}_get.json'.format(fn))
    def test_get(self, xm_test):
        for group in xm_test.groups_endpoint().get_groups():
            oncall_summ = xm_test.oncall_summary_endpoint().get_oncall_summary(groups=group.id)
            assert iter(oncall_summ)
            for o in oncall_summ:
                assert o.group.id is not None


class TestAccounting:

    @my_vcr.use_cassette('{}_get.json'.format(fn))
    def test_types(self, xm_test):
        for group in xm_test.groups_endpoint().get_groups():
            oncall_summs = xm_test.oncall_summary_endpoint().get_oncall_summary(groups=group.id)
            for o in oncall_summs:
                assert o.recipient.recipient_type in xmatters.factories.RecipientFactory._factory_objects.keys()

    @my_vcr.use_cassette('{}_get.json'.format(fn))
    def test_attrs(self, xm_test):
        for group in xm_test.groups_endpoint().get_groups():
            oncall_summs = xm_test.oncall_summary_endpoint().get_oncall_summary(groups=group.id)
            for o in oncall_summs:
                for k in o._api_data.keys():
                    snake_k = utils.camel_to_snakecase(k)
                    assert hasattr(o, snake_k)
