from tkinter import Tk
from .label_manager import LabelManager
from .button_manager import ButtonManager
from .dropdown_manager import DropdownManager
from .text_input_manager import TextInputManager
from .layout_manager import LayoutManager
from .progress_bar_manager import ProgressBarManager
from .container_manager import ContainerManager

class TKinterManager(object):
    def __init__(self, title, width=None, height=None):
        self.root = Tk()
        self.root.title(title)
        if width and height:
            self.root.geometry(f"{width}x{height}")
        self.elements_dict = {}
        self.layout_manager = LayoutManager(self.root)
    
    def run(self):
        self.root.mainloop()

    def add_element(self, element_name, element_type, label_text=None, hook_function=None, values=None):
        is_duplicate_element = element_name in self.elements_dict
        if is_duplicate_element:
            raise Exception(f"Multiple elements with name of '{element_name}' - rename your elements so they are unique.")

        label_name = f"{element_name}_label"
        label = LabelManager(self.root, label_name)

        if label_text:
            label.set(label_text)
            self.elements_dict[label_name] = label
        
        if element_type == "button":
            element = ButtonManager(self.root, element_name, hook_function)

        elif element_type == "dropdown":
            element = DropdownManager(self.root, element_name, values)

        elif element_type == "text_input":
            element = TextInputManager(self.root, element_name)

        elif element_type == "progress_bar":
            element = ProgressBarManager(self.root, element_name)

        elif element_type == "label":
            element = LabelManager(self.root, element_name)

        elif element_type in ["checkboxes", "radio_buttons"]:
            element = ContainerManager(self.root, element_name, element_type, values)

        self.elements_dict[element_name] = element

    def get_element(self, element_name):
        return self.elements_dict[element_name]

    def centre_elements(self):
        self.layout_manager.centre_elements(self.elements_dict)

    def set_layout(self, layout_schema):
        self.layout_manager.set_layout(layout_schema, self.elements_dict)