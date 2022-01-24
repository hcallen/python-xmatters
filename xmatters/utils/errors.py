import xmatters.common


class xMattersError(Exception):
    pass


class ApiError(xMattersError):
    def __init__(self, data):
        self.error = xmatters.common.Error(data) if data else None
        msg = '{} {} {}'.format(self.error.reason, self.error.code, self.error.message)
        super(ApiError, self).__init__(msg)
