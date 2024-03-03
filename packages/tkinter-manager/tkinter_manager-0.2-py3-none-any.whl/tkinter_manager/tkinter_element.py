class TKinterElement(object):
    def __init__(self, element_name, element_object, hook=None):
        self.name = element_name
        self.element_object = element_object
        self.hook = hook
