import urllib.parse

import xmatters.auth
import xmatters.connection
from xmatters.endpoints.endpoints import *


class xMattersSession(object):

    def __init__(self, base_url, **kwargs):
        """
        Primary class used to interact with xMatters API

        :param base_url: xMatters instance url or xMatters instance base url
        :type base_url: str
        """
        p_url = urllib.parse.urlparse(base_url)
        instance_url = 'https://{}'.format(p_url.netloc)
        self._base_url = '{}/api/xm/1'.format(instance_url)
        self.con = None
        self._kwargs = kwargs

    def set_authentication(self, username=None, password=None, client_id=None, token=None, token_storage=None):
        timeout = self._kwargs.get('timeout')
        max_retries = self._kwargs.get('max_retries')
        if client_id:
            self.con = xmatters.auth.OAuth2Auth(self._base_url, client_id, token, username, password, token_storage,
                                                timeout=timeout,
                                                max_retries=max_retries)
        elif None not in (username, password):
            self.con = xmatters.auth.BasicAuth(self._base_url, username, password, timeout=timeout,
                                               max_retries=max_retries)
        else:
            raise ValueError('unable to determine authentication method')

        return self

    @property
    def audits(self):
        return AuditsEndpoint(self)

    @property
    def conference_bridges(self):
        return ConferenceBridgesEndpoint(self)

    @property
    def device_names(self):
        return DeviceNamesEndpoint(self)

    @property
    def device_types(self):
        return DeviceTypesEndpoint(self)

    @property
    def devices(self):
        return DevicesEndpoint(self)

    @property
    def dynamic_teams(self):
        return DynamicTeamsEndpoint(self)

    @property
    def events(self):
        return EventsEndpoint(self)

    @property
    def event_suppressions(self):
        return EventSuppressionsEndpoint(self)

    @property
    def forms(self):
        return FormsEndpoint(self)

    @property
    def import_jobs(self):
        return ImportJobsEndpoint(self)

    @property
    def groups(self):
        return GroupsEndpoint(self)

    @property
    def incidents(self):
        return IncidentsEndpoint(self)

    @property
    def oncall(self):
        return OnCallEndpoint(self)

    @property
    def oncall_summary(self):
        return OnCallSummaryEndpoint(self)

    @property
    def people(self):
        return PeopleEndpoint(self)

    @property
    def plans(self):
        return PlansEndpoint(self)

    @property
    def roles(self):
        return RolesEndpoint(self)

    @property
    def scenarios(self):
        return ScenariosEndpoint(self)

    @property
    def services(self):
        return ServicesEndpoint(self)

    @property
    def sites(self):
        return SitesEndpoint(self)

    @property
    def subscriptions(self):
        return SubscriptionsEndpoint(self)

    @property
    def subscription_forms(self):
        return SubscriptionFormsEndpoint(self)

    @property
    def temporary_absences(self):
        return TemporaryAbsencesEndpoint(self)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
