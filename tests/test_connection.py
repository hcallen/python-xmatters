from xmatters.session import XMSession
from xmatters.utils import TokenFileStorage


# TODO: properly test
class TestErrors:

    def test_401_error(self, xm_test):
        xm_test.con.session.access_token = 'invalid-token'
        groups = xm_test.groups_endpoint().get_groups()
        assert iter(groups)
        assert xm_test.con.auth.session.token['access_token'] != 'invalid-token'


# TODO: Create separate tests; properly test
class TestKwargs:

    def test_basic_kwargs(self, settings):
        base_url = settings.get('test_base_url')
        username = 'null'
        password = 'null'
        xm = XMSession(base_url, timeout=11, max_retries=22, limit_per_request=33).set_authentication(username=username,
                                                                                                      password=password)
        assert xm.con.timeout == 11
        assert xm.con.max_retries == 22

    def test_oauth2_kwargs(self, settings):
        base_url = settings.get('test_base_url')
        client_id = settings.get('test_client_id')
        token_filepath = settings.get('test_token_filepath')
        ts = TokenFileStorage(token_filepath)
        xm = XMSession(base_url, timeout=11, max_retries=22, limit_per_request=33).set_authentication(
            client_id=client_id,
            token_storage=ts)
        assert xm.con.timeout == 11
        assert xm.con.max_retries == 22
