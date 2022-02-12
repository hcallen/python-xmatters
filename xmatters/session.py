import urllib.parse

import xmatters.auth
import xmatters.connection
import xmatters.endpoints
import xmatters.errors


class XMSession(object):
    """ Primary class used to interact with xMatters API """

    def __init__(self, base_url, **kwargs):
        """
        :param base_url: xMatters instance url or xMatters instance base url
        :type base_url: str
        :keyword timeout: timeout (in seconds) for requests, should be int. Defaults to 5.
        :keyword max_retries: maximum number of request retries to attempt, should be int. Defaults to 3.
            See :py:func:`xmatters.connection.Connection.max_retries` for HTTP status codes that trigger a retry.
        :keyword limit_per_request: maximum number of items returned from API request, should be int.
            Defaults to :py:const:`xmatters.utils.MAX_API_LIMIT`

        """
        p_url = urllib.parse.urlparse(base_url)
        instance_url = 'https://{}'.format(p_url.netloc) if p_url.netloc else 'https://{}'.format(p_url.path)
        self._base_url = '{}/api/xm/1'.format(instance_url)
        self.con = None
        self._kwargs = kwargs

    def set_authentication(self, username=None, password=None, client_id=None, token=None, token_storage=None):
        """
        Set authentication method to use.
            If client_id is provided, it is assumed OAuth2 authentication is desired;
            otherwise basic authentication is used.
        :param username: xMatters username
        :type username: str, optional
        :param password: xMatters password
        :type password: str, optional
        :param client_id: xMatters instance client id
        :type client_id: str, optional
        :param token: xMatters token object or refresh token
        :type token: dict or str, optional
        :param token_storage: Class instance used to store token returned during a refresh.
            Any class instance will be accepted as long as it has "read_token" and "write_token" methods.
        :type token_storage: :class:`xmatters.utils.TokenFileStorage`, optional
        :return: self
        :rtype: :class:`xmatters.session.XMSession`
        """

        if client_id:
            self.con = xmatters.auth.OAuth2Auth(self._base_url, client_id, token, username, password, token_storage,
                                                **self._kwargs)
        elif None not in (username, password):
            self.con = xmatters.auth.BasicAuth(self._base_url, username, password, **self._kwargs)
        else:
            raise xmatters.errors.AuthorizationError('unable to determine authentication method')

        # return self so method can be chained
        return self

    def audits(self):
        """
        Select the '/audits' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.AuditsEndpoint`
        """
        return xmatters.endpoints.AuditsEndpoint(self)

    def conference_bridges(self):
        """
        Select the '/conference-bridges' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.ConferenceBridgesEndpoint`
        """
        return xmatters.endpoints.ConferenceBridgesEndpoint(self)

    def device_names(self):
        """
        Select the '/device-names' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.DeviceNamesEndpoint`
        """
        return xmatters.endpoints.DeviceNamesEndpoint(self)

    def device_types(self):
        """
        Select the '/device-types' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.DeviceTypesEndpoint`
        """
        return xmatters.endpoints.DeviceTypesEndpoint(self)

    def devices(self):
        """
        Select the '/device' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.DevicesEndpoint`
        """
        return xmatters.endpoints.DevicesEndpoint(self)

    def dynamic_teams(self):
        """
        Select the '/dynamic-teams' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.DynamicTeamsEndpoint`
        """
        return xmatters.endpoints.DynamicTeamsEndpoint(self)

    def events(self):
        """
        Select the '/events' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.EventsEndpoint`
        """
        return xmatters.endpoints.EventsEndpoint(self)

    def event_suppressions(self):
        """
        Select the '/event-suppressions' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.EventSuppressionsEndpoint`
        """
        return xmatters.endpoints.EventSuppressionsEndpoint(self)

    def forms(self):
        """
        Select the '/forms' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.FormsEndpoint`
        """
        return xmatters.endpoints.FormsEndpoint(self)

    def import_jobs(self):
        """
        Select the '/import-jobs' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.ImportJobsEndpoint`
        """
        return xmatters.endpoints.ImportJobsEndpoint(self)

    def groups(self):
        """
        Select the '/groups' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.GroupsEndpoint`
        """
        return xmatters.endpoints.GroupsEndpoint(self)

    def incidents(self):
        """
        Select the '/incidents' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.IncidentsEndpoint`
        """
        return xmatters.endpoints.IncidentsEndpoint(self)

    def oncall(self):
        """
        Select the '/oncall' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.OnCallEndpoint`
        """
        return xmatters.endpoints.OnCallEndpoint(self)

    def oncall_summary(self):
        """
        Select the '/oncall-summary' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.OnCallSummaryEndpoint`
        """
        return xmatters.endpoints.OnCallSummaryEndpoint(self)

    def people(self):
        """
        Select the '/people' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.PeopleEndpoint`
        """
        return xmatters.endpoints.PeopleEndpoint(self)

    def plans(self):
        """
        Select the '/plans' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.PlansEndpoint`
        """
        return xmatters.endpoints.PlansEndpoint(self)

    def roles(self):
        """
        Select the '/roles' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.RolesEndpoint`
        """
        return xmatters.endpoints.RolesEndpoint(self)

    def scenarios(self):
        """
        Select the '/scenarios' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.ScenariosEndpoint`
        """
        return xmatters.endpoints.ScenariosEndpoint(self)

    def services(self):
        """
        Select the '/services' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.ServicesEndpoint`
        """
        return xmatters.endpoints.ServicesEndpoint(self)

    def sites(self):
        """
        Select the '/sites' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.SitesEndpoint`
        """
        return xmatters.endpoints.SitesEndpoint(self)

    def subscriptions(self):
        """
        Select the '/subscriptions' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.SubscriptionsEndpoint`
        """
        return xmatters.endpoints.SubscriptionsEndpoint(self)

    def subscription_forms(self):
        """
        Select the '/subscription-forms' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.SubscriptionsEndpoint`
        """
        return xmatters.endpoints.SubscriptionFormsEndpoint(self)

    def temporary_absences(self):
        """
        Select the '/temporary-absences' endpoint to interact with.

        :return: Class used to interact with endpoint.
        :rtype: :class:`xmatters.endpoints.TemporaryAbsencesEndpoint`
        """
        return xmatters.endpoints.TemporaryAbsencesEndpoint(self)

    # TODO
    # def upload_users(self):
    #     return xmatters.endpoints.UploadUsersEndpoint(self)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
