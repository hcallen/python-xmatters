import json
from xmatters import xMattersSession, TokenFileStorage
from .conftest import my_vcr
from requests_oauthlib.oauth2_session import TokenExpiredError


class TestAuth:

    @my_vcr.use_cassette('test_auth.json')
    def test_oauth_token_dict(self, settings):
        base_url = settings.get('base_url')
        client_id = settings.get('client_id')
        token_filepath = settings.get('token_filepath')
        with open(token_filepath, 'r') as f:
            token = json.load(f)
        try:
            xm_session = xMattersSession(base_url).set_authentication(client_id=client_id, token=token)
        except TokenExpiredError:
            xm_session = xMattersSession(base_url).set_authentication(client_id=client_id, token=token)
        assert isinstance(xm_session.con.token, dict)
        assert iter(xm_session.groups.get_groups())

    @my_vcr.use_cassette('test_auth.json')
    def test_oauth_token_refresh_token(self, settings):
        base_url = settings.get('base_url')
        client_id = settings.get('client_id')
        refresh_token = settings.get('refresh_token')
        try:
            xm_session = xMattersSession(base_url).set_authentication(client_id=client_id, token=refresh_token)
        except TokenExpiredError:
            xm_session = xMattersSession(base_url).set_authentication(client_id=client_id, token=refresh_token)
        assert isinstance(xm_session.con.token, dict)
        assert iter(xm_session.groups.get_groups())

    @my_vcr.use_cassette('test_auth.json')
    def test_oauth_token_username_password(self, settings):
        base_url = settings.get('base_url')
        client_id = settings.get('client_id')
        username = settings.get('username')
        password = settings.get('password')
        try:
            xm_session = xMattersSession(base_url).set_authentication(client_id=client_id, username=username, password=password)
        except TokenExpiredError:
            xm_session = xMattersSession(base_url).set_authentication(client_id=client_id, username=username, password=password)
        assert isinstance(xm_session.con.token, dict)
        assert iter(xm_session.groups.get_groups())

    @my_vcr.use_cassette('test_auth.json')
    def test_oauth_token_storage(self, settings):
        base_url = settings.get('base_url')
        client_id = settings.get('client_id')
        token_filepath = settings.get('token_filepath')
        ts = TokenFileStorage(token_filepath)
        try:
            xm_session = xMattersSession(base_url).set_authentication(client_id=client_id, token_storage=ts)
        except TokenExpiredError:
            xm_session = xMattersSession(base_url).set_authentication(client_id=client_id, token_storage=ts)
        assert isinstance(xm_session.con.token, dict)
        assert iter(xm_session.groups.get_groups())

    @my_vcr.use_cassette('test_auth.json')
    def test_basic(self, settings):
        base_url = settings.get('base_url')
        username = settings.get('username')
        password = settings.get('password')
        xm_session = xMattersSession(base_url).set_authentication(username=username, password=password)
        assert iter(xm_session.groups.get_groups())

