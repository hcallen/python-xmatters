from person import Person
from utils import ApiComponent


class xMattersSession(ApiComponent):
    _endpoints = {'get_people': '/people'}
    person_constructor = Person

    def __init__(self, parent):
        super(xMattersSession, self).__init__(parent)

    def get_people(self):
        xm_data = self.auth.get(self.build_url(self._endpoints.get('get_people'))).json()
        return [self.person_constructor(self, person) for person in xm_data.get('data')]
