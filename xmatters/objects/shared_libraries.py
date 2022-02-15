import xmatters.objects.plans


class SharedLibrary(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.script = data.get('script')
        plan = data.get('plan')
        self.plan = xmatters.objects.plans.PlanReference(plan) if plan else None