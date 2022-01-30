from xmatters.xm_objects.common import SelfLink
import xmatters.xm_objects.plans
from xmatters.connection import ApiBridge


class PlanConstant(ApiBridge):
    def __init__(self, parent, data):
        super(PlanConstant, self).__init__(parent, data)
        self.id = data.get('id')
        plan = data.get('plan')
        self.plan = xmatters.xm_objects.plans.PlanPointer(plan) if plan else None
        self.name = data.get('name')
        self.value = data.get('value')
        self.description = data.get('description')
        links = data.get('links')
        self.links = SelfLink(self, links) if links else None

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
