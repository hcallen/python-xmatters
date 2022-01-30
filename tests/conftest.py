import json

import pytest
import vcr
from xmatters.session import xMattersSession
from xmatters.utils import TokenFileStorage


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


@pytest.fixture(scope='session', autouse=False)
def xm(settings):
    base_url = settings.get('base_url')
    client_id = settings.get('client_id')
    token_filepath = settings.get('token_filepath')
    token_storage = TokenFileStorage(token_filepath)
    return xMattersSession(base_url).set_authentication(client_id=client_id, token_storage=token_storage)