import json

import pytest
import vcr
from xmatters.session import XMSession
from xmatters.utils import TokenFileStorage

SANDBOX = True


def skip_token_calls(request):
    if request.path.endswith('/oauth2/token'):
        return None
    else:
        return request


my_vcr = vcr.VCR(
    serializer='json',
    cassette_library_dir='../tests/cassettes',
    record_mode='new_episodes',
    match_on=['uri', 'method'],
    before_record_request=skip_token_calls
)


@pytest.fixture(scope='session')
def settings():
    with open('../tests/settings/settings.json', 'r') as f:
        return json.load(f)


@pytest.fixture(scope='session', autouse=True)
def xm_test(settings):
    base_url = settings.get('test_base_url')
    client_id = settings.get('test_client_id')
    token_filepath = settings.get('test_token_filepath')
    username = settings.get('test_username')
    password = settings.get('test_password')
    token_storage = TokenFileStorage(token_filepath)
    return XMSession(base_url).set_authentication(username=username, password=password, client_id=client_id,
                                                  token_storage=token_storage)


@pytest.fixture(scope='session', autouse=True)
def xm_sb(settings):
    base_url = settings.get('sb_base_url')
    client_id = settings.get('sb_client_id')
    token_filepath = settings.get('sb_token_filepath')
    username = settings.get('sb_username')
    password = settings.get('sb_password')
    token_storage = TokenFileStorage(token_filepath)
    return XMSession(base_url).set_authentication(username=username, password=password, client_id=client_id,
                                                  token_storage=token_storage)
