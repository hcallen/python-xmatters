import os

from tests.conftest import my_vcr
import xmatters.errors as err
from xmatters import utils

filename = os.path.basename(__file__).replace('.py', '')


class TestGet:
    @my_vcr.use_cassette('{}_get.json'.format(filename))
    def test_get(self, xm_test):
        forms = xm_test.forms_endpoint().get_forms()
        assert len(forms) > 0
        for form in forms:
            assert form.id is not None
            try:
                recipients = form.recipients
                assert iter(recipients)
                for r in recipients:
                    assert r.id is not None
                response_options = form.get_response_options()
                assert iter(response_options)
                for r in response_options:
                    assert r.id is not None
                sections = form.get_sections()
                assert iter(sections)
                for s in sections:
                    assert s.id is not None
                scenarios = form.get_scenarios()
                assert iter(scenarios)
                for s in scenarios:
                    assert s.id is not None
            except err.ForbiddenError:
                # skip forms that account doesn't have access to
                pass


class TestAccounting:
    @my_vcr.use_cassette('{}_get.json'.format(filename))
    def test_attrs(self, xm_test):
        forms = xm_test.forms_endpoint().get_forms()
        for form in forms:
            for k in form._api_data.keys():
                snake_k = utils.camel_to_snakecase(k)
                assert hasattr(form, snake_k)
            try:
                for i in form.get_recipients():
                    for k in i._api_data.keys():
                        snake_k = utils.camel_to_snakecase(k)
                        assert hasattr(i, snake_k)
                for i in form.get_response_options():
                    for k in i._api_data.keys():
                        snake_k = utils.camel_to_snakecase(k)
                        assert hasattr(i, snake_k)
                for i in form.get_sections():
                    for k in i._api_data.keys():
                        snake_k = utils.camel_to_snakecase(k)
                        assert hasattr(i, snake_k)
                for i in form.get_scenarios():
                    for k in i._api_data.keys():
                        snake_k = utils.camel_to_snakecase(k)
                        assert hasattr(i, snake_k)
            except err.ForbiddenError:
                # skip forms that account doesn't have access to
                pass
