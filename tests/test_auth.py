import json

from requests_oauthlib.oauth2_session import TokenExpiredError

from xmatters import XMSession, TokenFileStorage
from .conftest import my_vcr


class TestAuth:

    @my_vcr.use_cassette('test_auth.json')
    def test_oauth_token_dict(self, settings):
        base_url = settings.get('test_base_url')
        client_id = settings.get('test_client_id')
        token_filepath = settings.get('test_token_filepath')
        with open(token_filepath, 'r') as f:
            token = json.load(f)
        try:
            xm = XMSession(base_url).set_authentication(client_id=client_id, token=token)
        except TokenExpiredError:
            xm = XMSession(base_url).set_authentication(client_id=client_id, token=token)
        assert isinstance(xm.con.token, dict)
        assert iter(xm.groups().get_groups())

    @my_vcr.use_cassette('test_auth.json')
    def test_oauth_token_refresh_token(self, settings):
        base_url = settings.get('test_base_url')
        client_id = settings.get('test_client_id')
        refresh_token = settings.get('test_refresh_token')
        try:
            xm = XMSession(base_url).set_authentication(client_id=client_id, token=refresh_token)
        except TokenExpiredError:
            xm = XMSession(base_url).set_authentication(client_id=client_id, token=refresh_token)
        assert isinstance(xm.con.token, dict)
        assert iter(xm.groups().get_groups())

    @my_vcr.use_cassette('test_auth.json')
    def test_oauth_token_username_password(self, settings):
        base_url = settings.get('test_base_url')
        client_id = settings.get('test_client_id')
        username = settings.get('test_username')
        password = settings.get('test_password')
        try:
            xm = XMSession(base_url).set_authentication(client_id=client_id, username=username, password=password)
        except TokenExpiredError:
            xm = XMSession(base_url).set_authentication(client_id=client_id, username=username, password=password)
        assert isinstance(xm.con.token, dict)
        assert iter(xm.groups().get_groups())

    @my_vcr.use_cassette('test_auth.json')
    def test_oauth_token_storage(self, settings):
        base_url = settings.get('test_base_url')
        client_id = settings.get('test_client_id')
        token_filepath = settings.get('test_token_filepath')
        ts = TokenFileStorage(token_filepath)
        try:
            xm = XMSession(base_url).set_authentication(client_id=client_id, token_storage=ts)
        except TokenExpiredError:
            xm = XMSession(base_url).set_authentication(client_id=client_id, token_storage=ts)
        assert isinstance(xm.con.token, dict)
        assert iter(xm.groups().get_groups())

    @my_vcr.use_cassette('test_auth.json')
    def test_basic(self, settings):
        base_url = settings.get('test_base_url')
        username = settings.get('test_username')
        password = settings.get('test_password')
        xm = XMSession(base_url).set_authentication(username=username, password=password)
        assert iter(xm.groups().get_groups())

    def test_basic_kwargs(self, settings):
        base_url = settings.get('test_base_url')
        username = settings.get('test_username')
        password = settings.get('test_password')
        xm = XMSession(base_url, timeout=1, max_retries=2, limit_per_request=100).set_authentication(username=username,
                                                                                                     password=password)
        assert xm.con.timeout == 1
        assert xm.con.max_retries == 2
        assert xm.con.limit_per_request == 100

    def test_oauth2_kwargs(self, settings):
        base_url = settings.get('test_base_url')
        client_id = settings.get('test_client_id')
        token_filepath = settings.get('test_token_filepath')
        ts = TokenFileStorage(token_filepath)
        try:
            xm = XMSession(base_url, timeout=1, max_retries=2, limit_per_request=100).set_authentication(
                client_id=client_id,
                token_storage=ts)
        except TokenExpiredError:
            xm = XMSession(base_url, timeout=1, max_retries=2, limit_per_request=100).set_authentication(
                client_id=client_id,
                token_storage=ts)
        assert xm.con.timeout == 1
        assert xm.con.max_retries == 2
        assert xm.con.limit_per_request == 100
