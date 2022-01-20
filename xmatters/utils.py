class ApiComponent(object):
    def __init__(self, parent, data=None):
        self.base_url = parent.base_url

        if data and 'links' in data.keys():
            self_link = data.get('links').get('self').replace('/api/xm/1', '')
            self.base_resource = '{}{}'.format(parent.base_url, self_link)
        else:
            self.base_resource = parent.base_url

        self.s = parent.s if hasattr(parent, 's') else parent

    def build_url(self, endpoint):
        return '{}{}'.format(self.base_resource, endpoint)
