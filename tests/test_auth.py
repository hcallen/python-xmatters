import json

from xmatters import xMattersSession, OAuth2Auth, TokenFileStorage
from xmatters.common import Pagination
from .conftest import my_vcr


class TestSession:

    @my_vcr.use_cassette('test_session.json')
    def test_oauth_token_dict(self, settings):
        base_url = settings.get('base_url')
        client_id = settings.get('client_id')
        token_filepath = settings.get('token_filepath')
        with open(token_filepath, 'r') as f:
            token = json.load(f)
        auth = OAuth2Auth(client_id=client_id, token=token)
        xm_session = xMattersSession(base_url, auth)
        assert isinstance(xm_session.con.token, dict)
        groups = xm_session.get_groups()
        assert isinstance(groups, Pagination) or isinstance(groups, list)

    @my_vcr.use_cassette('test_session.json')
    def test_oauth_token_str(self, settings):
        base_url = settings.get('base_url')
        refresh_token = settings.get('refresh_token')
        client_id = settings.get('client_id')
        auth = OAuth2Auth(client_id=client_id, token=refresh_token)
        xm_session = xMattersSession(base_url, auth)
        assert isinstance(xm_session.con.token, dict)
        groups = xm_session.get_groups()
        assert isinstance(groups, Pagination) or isinstance(groups, list)

    @my_vcr.use_cassette('test_session.json')
    def test_oauth_username_and_password(self, settings):
        base_url = settings.get('base_url')
        username = settings.get('username')
        password = settings.get('password')
        client_id = settings.get('client_id')
        auth = OAuth2Auth(client_id=client_id, username=username, password=password)
        xm_session = xMattersSession(base_url, auth)
        assert isinstance(xm_session.con.token, dict)
        groups = xm_session.get_groups()
        assert isinstance(groups, Pagination) or isinstance(groups, list)

    @my_vcr.use_cassette('test_session.json')
    def test_oauth_token_storage(self, settings):
        base_url = settings.get('base_url')
        client_id = settings.get('client_id')
        token_filepath = settings.get('token_filepath')
        token_storage = TokenFileStorage(token_filepath)
        auth = OAuth2Auth(client_id=client_id, token_storage=token_storage)
        xm_session = xMattersSession(base_url, auth)
        assert isinstance(xm_session.con.token, dict)
        groups = xm_session.get_groups()
        assert isinstance(groups, Pagination) or isinstance(groups, list)

    def test_token_set(self):
        auth = OAuth2Auth(client_id='some_client_id', token='12345')
        assert auth.token == '12345'
        auth.token = '54321'
        assert auth.token == '54321'
