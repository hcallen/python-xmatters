import xmatters.objects.plans


class SharedLibrary(object):
    def __init__(self, data):
        self.id = data.get('id')    #: :vartype: str
        self.name = data.get('name')    #: :vartype: str
        self.script = data.get('script')   #: :vartype: str
        plan = data.get('plan')
        self.plan = xmatters.objects.plans.PlanReference(plan) if plan else None    #: :vartype: :class:`~xmatters.objects.plans.PlanReference`
