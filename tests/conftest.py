import json

import pytest
import vcr
from xmatters.session import xMattersSession
from xmatters.utils.connection import xOAuth2Session
from xmatters.utils.utils import TokenFileStorage


def skip_token_calls(request):
    if request.path.endswith('/oauth2/token'):
        return None
    else:
        return request


my_vcr = vcr.VCR(
    serializer='json',
    cassette_library_dir='./tests/cassettes',
    record_mode='once',
    match_on=['uri', 'method'],
    before_record_request=skip_token_calls
)


@pytest.fixture(scope='session')
def settings():
    with open('./tests/settings/settings.json', 'r') as f:
        return json.load(f)


@pytest.fixture(scope='session', autouse=True)
def xm_session(settings):
    base_url = settings.get('base_url')
    client_id = settings.get('client_id')
    token_filepath = settings.get('token_filepath')
    token_store = TokenFileStorage(token_filepath)
    auth = xOAuth2Session(base_url=base_url, client_id=client_id, token_storage=token_store)
    return xMattersSession(base_url, auth=auth)


@pytest.fixture(scope='function')
def pagination_factory():
    def _pagination(api_object, method_name):
        method = getattr(api_object, method_name)
        pagination = method()
        for _ in pagination:
            pass
    return _pagination
