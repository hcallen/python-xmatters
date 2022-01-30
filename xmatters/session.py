import urllib.parse

import xmatters.auth
import xmatters.connection
from xmatters.endpoints import *


class XMSession(object):

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

    def audits(self):
        return AuditsEndpoint(self)

    def conference_bridges(self):
        return ConferenceBridgesEndpoint(self)

    def device_names(self):
        return DeviceNamesEndpoint(self)

    def device_types(self):
        return DeviceTypesEndpoint(self)

    def devices(self):
        return DevicesEndpoint(self)

    def dynamic_teams(self):
        return DynamicTeamsEndpoint(self)

    def events(self):
        return EventsEndpoint(self)

    def event_suppressions(self):
        return EventSuppressionsEndpoint(self)

    def forms(self):
        return FormsEndpoint(self)

    def import_jobs(self):
        return ImportJobsEndpoint(self)

    def groups(self):
        return GroupsEndpoint(self)

    def incidents(self):
        return IncidentsEndpoint(self)

    def oncall(self):
        return OnCallEndpoint(self)

    def oncall_summary(self):
        return OnCallSummaryEndpoint(self)

    def people(self):
        return PeopleEndpoint(self)

    def plans(self):
        return PlansEndpoint(self)

    def roles(self):
        return RolesEndpoint(self)

    def scenarios(self):
        return ScenariosEndpoint(self)

    def services(self):
        return ServicesEndpoint(self)

    def sites(self):
        return SitesEndpoint(self)

    def subscriptions(self):
        return SubscriptionsEndpoint(self)

    def subscription_forms(self):
        return SubscriptionFormsEndpoint(self)

    def temporary_absences(self):
        return TemporaryAbsencesEndpoint(self)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
