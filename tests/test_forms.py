from tests.conftest import my_vcr


class TestForms:
    @my_vcr.use_cassette('test_forms.json')
    def test_forms(self, xm):
        forms = list(xm.forms().get_forms())
        for form in forms:
            assert iter(list(form.recipients))
            assert iter(list(form.get_response_options()))
            assert iter(list(form.get_sections()))
            assert iter(list(form.get_scenarios()))
