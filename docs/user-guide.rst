User Guide
===========

Initial Setup
_____________

A typical session starts by initializing an XMSession class with an xMatters instance url.

Example:

.. code-block:: python

    from xmatters import XMSession

    xm_session = XMSession('my-instance.xmatters.com')



Authentication
--------------

Both basic and OAuth2 authentication are supported.

The authentication mechanism is set using :meth:`xmatters.XMSession.set_authentication`. Whether to use basic or OAuth2
authentication is implied. If the *client_id* parameter is defined, OAuth2 is used, otherwise basic is used.

Basic Authentication
^^^^^^^^^^^^^^^^^^^^

Example:

.. code-block:: python

    from xmatters import XMSession

    xm_session = XMSession('my-instance.xmatters.com')
    xm_session.set_authentication(username='my-username', password='my-password')

OAuth2 Authentication
^^^^^^^^^^^^^^^^^^^^^

Example using username and password:

.. code-block:: python

    from xmatters import XMSession

    xm_session = XMSession('my-instance.xmatters.com')
    xm_session.set_authentication(username='my-username', password='my-password', client_id='my-client-id)

Example using token dictionary:

.. code-block:: python

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

    xm_session = XMSession('my-instance.xmatters.com')
    xm_session.set_authentication(client_id='my-client-id', token=my_token)


Example using refresh token:

.. code-block:: python

    from xmatters import XMSession

    xm_session = XMSession('my-instance.xmatters.com')
    xm_session.set_authentication(client_id='my-client-id', refresh_token='my-refresh-token')

Example using token storage

.. note::
    :class:`xmatters.utils.TokenFileStorage` is used in this example. Any object with **read_token** and
    **write_token** methods can be used.

.. code-block:: python

    from xmatters import XMSession
    from xmatters.utils import TokenFileStorage

    token_storage = TokenFileStorage('/path/to/my_token.json')
    xm_session = XMSession('my_instance.xmatters.com')
    xm_session.set_authentication(client_id='my-client-id', token_storage=token_storage)


Accessing Endpoints
-------------------

Top-level endpoints can be accessed by using :meth:`xmatters.XMSession.get_endpoint`

Example:

.. code-block:: python

    people_endpoint = xm_session.get_endpoint('people')
    people = people_endpoint.get_people()

    for person in people:
        devices = person.get_devices()
        for device in devices:
            print(device.target_name)



.. note::

    Object specific endpoints can be accessed from the respective object. Refer to :ref:`api:xMatters API Objects` for
    methods to access an object endpoint.


Top-level endpoints can also be accessed by calling a number of :class:`xmatters.XMSession` helper methods

Example:

.. code-block:: python

    people = xm_session.people_endpoint().get_people()

    for person in people:
        devices = person.get_devices()
        for device in devices:
            print(device.target_name)



Query Parameters
----------------

.. note::
    Refer to the `xMatters REST API Reference <https://help.xmatters.com/xmapi/>`_ for valid parameters and arguments.

Params
^^^^^^

Query parameters can be applied to *GET* requests by passing a dict to the *params* parameter for the applicable method.

Example:

.. code-block:: python

    # get all active people with devices
    params = {'devices.exists': True,
              'status': 'ACTIVE'}
    people = xm_session.people_endpoint().get_people(params)

    for person in people:
        print(person.target_name)



Kwargs
^^^^^^

Query parameters can also be passed as kwargs.

Example:

.. code-block:: python

    # get groups sorted by status in descending order
    groups = xm_session.groups_endpoint().get_groups(sortBy='STATUS', sortOrder='DESCENDING')

    for group in groups:
        print(group.target_name)

.. note::

    | Parameters that use a Python reserved keyword for their name by appending (or prepending)
        an underscore to their name.
    | Example: *from* parameter can be a kwarg as *from_*


Parameter Casing
^^^^^^^^^^^^^^^^

Query parameters can also be snake-cased.

Example:

.. code-block:: python

    # get groups sorted by status in descending order
    groups = xm_session.groups_endpoint().get_groups(sort_by='STATUS', sort_order='DESCENDING')

    for group in groups:
        print(group.target_name)

.. note::

    | Parameters containing a period can be passed as snake-case by replacing the period
        with '_dot_'
    | Example: *devices.exists* parameter can be a kwarg as *devices_dot_exists*

Timestamp Parameters
^^^^^^^^^^^^^^^^^^^^

Query parameters that expect a ISO-8601 UTC timestamp have the UTC offset of your local timezone applied
if the UTC timezone isn't included in the timestamp.

The timestamps are also formatted to a proper ISO-8601 timestamp if only partially provided.

Example:

.. code-block:: python

    # the arguments will be updated to '2022-01-01T08:00:00+00:00' and '2022-02-01T08:00:00+00:00'
    # in respect to my local timezone (Pacific)
    events = xm_session.events_endpoint().get_events(from_='2022-01-01', to='2022-02-01')