# python-xmatters

python-xmatters is a wrapper for the xMatters API. It is very much still in development and only GET requests are
currently implemented.

## Features

- Most (if not all) endpoints and objects implemented.
- Support for both basic and OAuth2 authentication.
- Auto-refresh of access tokens and storage for token objects.
- Support for pagination objects.
- Conversion to datetime objects (local or UTC timezone) for time attributes.

## Requirements

- [Python 3.5+](http://python.org)
- Installation of package requirements.

  ```$ python3 -m pip install -r requirements.txt```

## Usage

Review source code and the [xMatters REST API Reference](https://help.xmatters.com/xmapi/)
for methods and parameters.

### Basic Authentication

```python
from xmatters import XMSession

xm = XMSession('my_instance.xmatters.com')
xm.set_authentication(username='my_username', password='my_password')
groups = xm.groups()
for group in groups.get_groups():
    print(group.target_name)
```

### OAuth2 Authentication
It is assumed that if a client_id is provided; OAuth2 authentication is desired.

#### Using refresh token
```python
from xmatters import XMSession
refresh_token = 'my-refresh-token'
xm = XMSession('my_instance.xmatters.com')
xm.set_authentication(client_id='my-client-id', token=refresh_token)
groups = xm.groups()
for group in groups.get_groups():
    print(group.target_name)
```
#### Using token object
```python
from xmatters import XMSession
my_token = {
    "access_token": "my-access-token",
    "token_type": "bearer",
    "refresh_token": "my-refresh-token",
    "expires_in": 900,
    "jti": "my-jti",
    "sbu": "my-sbu",
    "expires_at": 0123456789.012345
}
xm = XMSession('my_instance.xmatters.com')
xm.set_authentication(client_id='my-client-id', token=my_token)
groups = xm.groups()
for group in groups.get_groups():
    print(group.target_name)
```
#### Using username and password with token storage
Any class instance with read_token and write_token methods should work as token_storage
```python
from xmatters import XMSession, TokenFileStorage
token_storage = TokenFileStorage('/path/to/my_token.json')
xm = XMSession('my_instance.xmatters.com')
xm.set_authentication(client_id='my-client-id', username='my_username', password='my_password', token_storage=token_storage)
groups = xm.groups()
for group in groups.get_groups():
    print(group.target_name)
```

### Date conversion to local timezone
```python
from xmatters import XMSession, TokenFileStorage
token_storage = TokenFileStorage('/path/to/my_token.json')
xm = XMSession('my_instance.xmatters.com')
xm.set_authentication(client_id='my-client-id', token_storage=token_storage)
groups = xm.groups()
for group in groups.get_groups():
    print(group.created.local_datetime().isoformat())
```
