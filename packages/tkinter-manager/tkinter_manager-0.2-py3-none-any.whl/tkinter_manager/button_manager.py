from .tkinter_element import TKinterElement
from tkinter.ttk import Button
from .utils import return_clean_text

class ButtonManager(TKinterElement):
    def __init__(self, root, element_name, hook_function):
        TKinterElement.__init__(self, element_name, Button(root, text=return_clean_text(element_name)))
        self.set_hook(hook_function)

    def set_hook(self, input_function):
        self.element_object.configure(command=input_function)