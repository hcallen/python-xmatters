import json
from datetime import datetime, timedelta

import pytest
import vcr
from dateutil.relativedelta import relativedelta

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


@pytest.fixture(scope='session')
def xm_test(settings):
    base_url = settings.get('test_base_url')
    client_id = settings.get('test_client_id')
    token_filepath = settings.get('test_token_filepath')
    username = settings.get('test_username')
    password = settings.get('test_password')
    token_storage = TokenFileStorage(token_filepath)
    return XMSession(base_url).set_authentication(username=username, password=password, client_id=client_id,
                                                  token_storage=token_storage)


@pytest.fixture(scope='session')
def xm_sb(settings):
    base_url = settings.get('sb_base_url')
    client_id = settings.get('sb_client_id')
    token_filepath = settings.get('sb_token_filepath')
    username = settings.get('sb_username')
    password = settings.get('sb_password')
    token_storage = TokenFileStorage(token_filepath)
    return XMSession(base_url).set_authentication(username=username, password=password, client_id=client_id,
                                                  token_storage=token_storage)


@pytest.fixture(scope='session')
def xm_prod(settings):
    base_url = settings.get('prod_base_url')
    client_id = settings.get('prod_client_id')
    token_filepath = settings.get('prod_token_filepath')
    refresh_token = settings.get('prod_refresh_token')
    token_storage = TokenFileStorage(token_filepath)
    return XMSession(base_url).set_authentication(client_id=client_id, token=refresh_token, token_storage=token_storage)


@pytest.fixture(scope='session')
@my_vcr.use_cassette('events_last_month.json')
def events_last_month(xm_test):
    start_dt = (datetime.now() - relativedelta(months=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_dt = ((start_dt + relativedelta(months=1)) - timedelta(microseconds=1))
    from_time = start_dt.isoformat()
    to_time = end_dt.isoformat()
    return xm_test.events().get_events(from_time=from_time, to_time=to_time, sort_order='DESCENDING',
                                       sort_by='START_TIME')
