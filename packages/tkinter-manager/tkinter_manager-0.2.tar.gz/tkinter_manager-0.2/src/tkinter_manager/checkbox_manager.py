from .tkinter_element import TKinterElement
from tkinter.ttk import Checkbutton
from tkinter import StringVar

class CheckboxManager(TKinterElement):
    def __init__(self, root, element_name, value):
        self.state = StringVar()
        TKinterElement.__init__(self, element_name, Checkbutton(root, text=value, variable=self.state))

    def get(self):
        return self.state.get()
    
    def set(self, value):
        self.state.set(value)