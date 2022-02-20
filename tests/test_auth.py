import json

from xmatters.session import XMSession
from xmatters.utils import TokenFileStorage
from .conftest import my_vcr


class TestAuth:

    @my_vcr.use_cassette('test_auth.json')
    def test_oauth_token_dict(self, settings):
        base_url = settings.get('test_base_url')
        client_id = settings.get('test_client_id')
        token_filepath = settings.get('test_token_filepath')
        with open(token_filepath, 'r') as f:
            token = json.load(f)
        xm = XMSession(base_url).set_authentication(client_id=client_id, token=token)
        assert isinstance(xm._con.token, dict)
        assert iter(list(xm.groups_endpoint().get_groups()))

    @my_vcr.use_cassette('test_auth.json')
    def test_oauth_token_refresh_token(self, settings):
        base_url = settings.get('test_base_url')
        client_id = settings.get('test_client_id')
        refresh_token = settings.get('test_refresh_token')
        xm = XMSession(base_url).set_authentication(client_id=client_id, refresh_token=refresh_token)
        assert isinstance(xm._con.token, dict)
        assert iter(list(xm.groups_endpoint().get_groups()))

    @my_vcr.use_cassette('test_auth.json')
    def test_oauth_token_username_password(self, settings):
        base_url = settings.get('test_base_url')
        client_id = settings.get('test_client_id')
        username = settings.get('test_username')
        password = settings.get('test_password')
        xm = XMSession(base_url).set_authentication(client_id=client_id, username=username, password=password)
        assert isinstance(xm._con.token, dict)
        assert iter(list(xm.groups_endpoint().get_groups()))

    @my_vcr.use_cassette('test_auth.json')
    def test_oauth_token_storage(self, settings):
        base_url = settings.get('test_base_url')
        client_id = settings.get('test_client_id')
        token_filepath = settings.get('test_token_filepath')
        ts = TokenFileStorage(token_filepath)
        xm = XMSession(base_url).set_authentication(client_id=client_id, token_storage=ts)
        assert isinstance(xm._con.token, dict)
        assert iter(list(xm.groups_endpoint().get_groups()))

    @my_vcr.use_cassette('test_auth.json')
    def test_basic(self, settings):
        base_url = settings.get('test_base_url')
        username = settings.get('test_username')
        password = settings.get('test_password')
        xm = XMSession(base_url).set_authentication(username=username, password=password)
        assert iter(list(xm.groups_endpoint().get_groups()))




