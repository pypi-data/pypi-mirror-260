from .tkinter_element import TKinterElement
from tkinter.ttk import Progressbar

class ProgressBarManager(TKinterElement):
    def __init__(self, root, element_name):
        TKinterElement.__init__(self, element_name, Progressbar(root))

    def get(self, decimal_places=0):
        return round(self.element_object['value'], decimal_places)
    
    def set(self, value):
        self.element_object['value'] = int(value) / 100

    def start(self):
        self.element_object.start()

    def stop(self):
        self.element_object.stop()