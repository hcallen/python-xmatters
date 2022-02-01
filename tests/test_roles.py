from .conftest import my_vcr


class TestRoles:

    @my_vcr.use_cassette('test_roles.json')
    def test_roles(self, xm_test):
        roles = list(xm_test.roles().get_roles())
        assert iter(roles)
