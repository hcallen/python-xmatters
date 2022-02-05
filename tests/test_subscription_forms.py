from tests.conftest import my_vcr


class TestSubscriptionForms:

    @my_vcr.use_cassette('test_subscription_forms.json')
    def test_subscription_forms(self, xm_test):
        forms = list(xm_test.subscription_forms().get_subscription_forms())
        for form in forms:
            assert form.id is not None
            assert iter(list(form.target_device_names))
            assert iter(list(form.visible_target_device_names))
            assert iter(list(form.property_definitions))
            assert iter(list(form.roles))

