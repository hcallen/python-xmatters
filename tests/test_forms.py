from tests.conftest import my_vcr
import xmatters.errors as err


class TestForms:
    @my_vcr.use_cassette('test_forms.json')
    def test_forms(self, xm_test):
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
