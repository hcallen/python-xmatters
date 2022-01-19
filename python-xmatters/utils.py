class ApiComponent(object):
    def __init__(self, parent):
        self.base_resource = parent.base_resource if not parent.base_resource.endswith('/') else parent.base_resource[
                                                                                                 :-1]
        self.auth = parent

    def build_url(self, endpoint):
        return '{}{}'.format(self.base_resource, endpoint)
