#TODO: property types

class Property(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.property_type = data.get('propertyType')
        self.name = data.get('name')
        self.description = data.get('description')
        self.help_text = data.get('helpText')