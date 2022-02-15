Installation
============

Requirements
------------

Python >=3.5

Install python-xmatters
-----------------------

Install using pip:

.. code-block:: bash

  $ pip install pytest-xmatters



Quick Start
===========

The expected workflow is:

#. Import and initialize XMSession with an xMatters instance url.
#. Set the desired authentication method.
#. Initialize an endpoint.
#. Execute a method on the endpoint.

Example using basic authentication:

.. code-block:: python

    from xmatters import XMSession

    xm = XMSession('my-instance.xmatters.com')
    xm_session.set_authentication(username='my_username', password='my_password')

    people_endpoint = xm_session.get_endpoint('people')
    people = people_endpoint.get_people()

    for person in people:
        print(person.target_name)

Example using OAuth2 authentication with refresh token:

.. code-block:: python

    from xmatters import XMSession

    xm_session = XMSession('my-instance.xmatters.com')
    xm_session.set_authentication(client_id='my-client-id', refresh_token='my-refresh-token')

    people_endpoint = xm_session.get_endpoint('people')
    people = people_endpoint.get_people()

    for person in people:
        print(person.target_name)

.. note::

    | The use of OAuth2 authentication is implied if client_id is provided.







