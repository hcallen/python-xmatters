import xmatters.common


class Error(Exception):
    pass


class xMattersError(Error):
    def __init__(self, msg):
        super(xMattersError, self).__init__(msg)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class AuthorizationError(Error):
    def __init__(self, data):
        msg = '{} - {}'.format(data.get('error'), data.get('error_description'))
        super(AuthorizationError, self).__init__(msg)


class ResponseError(Error):
    def __init__(self, response):
        msg = '{} - {} - {}'.format(response.url, response.status_code, response.reason)
        super(ResponseError, self).__init__(msg)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


class ApiError(Error):
    def __init__(self, data):
        self.error = xmatters.common.Error(data) if data else None
        msg = '{} {} {}'.format(self.error.reason, self.error.code, self.error.message)
        super(ApiError, self).__init__(msg)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
