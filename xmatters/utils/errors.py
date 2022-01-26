import xmatters.common


class Error(Exception):
    pass



class ApiError(Error):
    def __init__(self, data):
        self.error = xmatters.common.Error(data) if data else None
        msg = '{} {} {}'.format(self.error.reason, self.error.code, self.error.message)
        super(ApiError, self).__init__(msg)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()


