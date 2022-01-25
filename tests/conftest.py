import json

import betamax
import pytest

from xmatters.session import xMattersSession
from xmatters.utils.connection import OAuth2
from xmatters.utils.utils import TokenFileStorage

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = './tests/cassettes'


@pytest.fixture(scope='session', autouse=True)
def settings():
    with open('./tests/settings/settings.json', 'r') as f:
        return json.load(f)


@pytest.fixture(scope='session', autouse=True)
def xm_session(settings):
    base_url = settings.get('base_url')
    client_id = settings.get('client_id')
    token_filepath = settings.get('token_filepath')
    token_store = TokenFileStorage(token_filepath)
    auth = OAuth2(base_url=base_url, client_id=client_id, token_storage=token_store)
    yield xMattersSession(auth=auth)
