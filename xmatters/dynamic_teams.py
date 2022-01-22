from xmatters.common import Recipient


class DynamicTeam(Recipient):
    def __init__(self, parent, data):
        super(DynamicTeam, self).__init__(parent, data)
        self.response_count = data.get('responseCount')
        self.response_count_threshold = data.get('responseCountThreshold')
        self.use_emergency_device = data.get('useEmergencyDevice')
