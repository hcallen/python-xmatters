import json

import pytest
import vcr


import xmatters.utils
from xmatters.session import XMSession

def skip_token_calls(request):
    if request.path.endswith('/oauth2/token'):
        return None
    else:
        return request


# def skip_timeouts(request):
#     if request.get('status', {}).get('code') == 504:
#         return None
#     else:
#         return request


my_vcr = vcr.VCR(
    serializer='json',
    cassette_library_dir='../tests/cassettes',
    record_mode='new_episodes',
    match_on=['uri', 'method'],
    before_record_request=skip_token_calls
)


@pytest.fixture(scope='session')
def settings():
    try:
        with open('../tests/settings/settings.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        with open('./tests/settings/settings.json', 'r') as f:
            return json.load(f)


@pytest.fixture(scope='session')
def xm_test(settings):
    base_url = settings.get('test_base_url')
    client_id = settings.get('test_client_id')
    token_filepath = settings.get('test_token_filepath')
    token_storage = xmatters.utils.TokenFileStorage(token_filepath)
    xm = XMSession(base_url, timeout=60, max_retries=3)
    return xm.set_authentication(client_id=client_id, token_storage=token_storage)


@pytest.fixture(scope='session')
def xm_sb(settings):
    base_url = settings.get('sb_base_url')
    client_id = settings.get('sb_client_id')
    token_filepath = settings.get('sb_token_filepath')
    token_storage = xmatters.utils.TokenFileStorage(token_filepath)
    return XMSession(base_url).set_authentication(client_id=client_id,token_storage=token_storage)


@pytest.fixture(scope='session')
def xm_prod(settings):
    base_url = settings.get('prod_base_url')
    client_id = settings.get('prod_client_id')
    token_filepath = settings.get('prod_token_filepath')
    token_storage = xmatters.utils.TokenFileStorage(token_filepath)
    return XMSession(base_url).set_authentication(client_id=client_id,token_storage=token_storage)
