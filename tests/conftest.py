import json

import pytest
from betamax import Betamax
from betamax_serializers import pretty_json

from xmatters.session import xMattersSession
from xmatters.utils.connection import OAuth2
from xmatters.utils.utils import TokenFileStorage


def skip_token_calls(interaction, current_cassette):
    if interaction.data['request']['uri'].endswith('/oauth2/token'):
        interaction.ignore()


Betamax.register_serializer(pretty_json.PrettyJSONSerializer)
with Betamax.configure() as config:
    config.cassette_library_dir = '../tests/cassettes'
    config.default_cassette_options['serialize_with'] = 'prettyjson'
    config.before_record(callback=skip_token_calls)
    config.before_playback(callback=skip_token_calls)

@pytest.fixture(scope='session')
def settings():
    with open('../tests/settings/settings.json', 'r') as f:
        return json.load(f)


@pytest.fixture(scope='session', autouse=True)
def xm_session(settings):
    base_url = settings.get('base_url')
    client_id = settings.get('client_id')
    token_filepath = settings.get('token_filepath')
    token_store = TokenFileStorage(token_filepath)
    auth = OAuth2(base_url=base_url, client_id=client_id, token_storage=token_store)
    return xMattersSession(auth=auth)


@pytest.fixture(scope='function')
def pagination_factory():
    def _pagination(api_object, method_name):
        page_index = 0
        recorder = Betamax(api_object.con.session)
        recorder.use_cassette('{}_page_{}'.format(method_name, page_index))
        recorder.start()
        method = getattr(api_object, method_name)
        pagination = method()
        recorder.stop()
        recorder.session = pagination.con.session
        for _ in pagination:
            if pagination.index == (pagination.count - 1):
                recorder.stop()
            if pagination.index == pagination.count and pagination.links and pagination.links.next:
                page_index += 1
                recorder.use_cassette('{}_page_{}'.format(method_name, page_index))
                recorder.start()

    return _pagination
