from tests.conftest import my_vcr
import xmatters.errors as err

class TestForms:
    @my_vcr.use_cassette('test_forms.json')
    def test_forms(self, xm_test):
        forms = list(xm_test.forms().get_forms())
        assert len(forms) > 0
        for form in forms:
            assert form.id is not None
            try:
                assert iter(list(form.recipients))
                assert iter(list(form.get_response_options()))
                assert iter(list(form.get_sections()))
                assert iter(list(form.get_scenarios()))
            except err.ForbiddenError:
                # skip forms that account doesn't have access to
                pass
