from .tkinter_element import TKinterElement
from tkinter.ttk import Frame
from tkinter import StringVar
from .checkbox_manager import CheckboxManager
from .radio_button_manager import RadioButtonManager

class ContainerManager(TKinterElement):
    def __init__(self, root, element_name, children_type, values):
        self.root = root
        self.children_type = children_type
        self.children_dict = {}
        TKinterElement.__init__(self, element_name, Frame(root))
        self.set(values)

    def get(self, checkbox_name):
        return self.children_dict[checkbox_name]
    
    def set(self, values):
        if self.children_type == "checkboxes":
            for value in values:
                child_name = f"{value}_checkbox"
                child = CheckboxManager(self.element_object, child_name, value)

                self.children_dict[value] = child
                child.element_object.pack()

        elif self.children_type == "radio_buttons":
            self.state = StringVar()
            for value in values:
                child_name = f"{value}_radio_button"
                child = RadioButtonManager(self.element_object, child_name, value, self.state)

                self.children_dict[value] = child
                child.element_object.pack()

    def get_children_names(self):
        return list(self.children_dict.keys())
    
    def get_selected(self):
        if self.children_type == "checkboxes":
            selected_values = []
            for child_name, child in self.children_dict.items():
                is_selected = child.get()
                if is_selected:
                    selected_values.append(child_name)
            return selected_values
        elif self.children_type == "radio_buttons":
            return self.state.get()
