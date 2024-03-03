from .tkinter_element import TKinterElement
from tkinter.ttk import Combobox

class DropdownManager(TKinterElement):
    def __init__(self, root, element_name, input_list):
        TKinterElement.__init__(self, element_name, Combobox(root))
        self.set(input_list)

    def set(self, input_values):
        self.element_object['values'] = input_values

    def get(self):
        return self.element_object.get()