from tests.conftest import my_vcr
from xmatters.endpoints.common import Pagination


class TestForms:

    @my_vcr.use_cassette('test_get_forms.json')
    def test_get_forms(self, xm_session):
        forms = xm_session.get_forms()
        assert isinstance(forms, Pagination) or isinstance(forms, list)

    @my_vcr.use_cassette('test_get_forms_recipients.json')
    def test_get_forms_recipients(self, xm_session):
        forms = xm_session.get_forms()
        for form in forms:
            r = form.recipients
            assert isinstance(forms, Pagination) or isinstance(forms, list)

    @my_vcr.use_cassette('test_get_forms_response_options.json')
    def test_get_forms_response_options(self, xm_session):
        forms = xm_session.get_forms()
        for form in forms:
            r = form.response_options
            assert isinstance(r, Pagination) or isinstance(r, list)
