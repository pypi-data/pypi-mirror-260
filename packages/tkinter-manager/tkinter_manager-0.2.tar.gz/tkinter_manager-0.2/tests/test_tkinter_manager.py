from tkinter_manager.tkinter_manager import TKinterManager
from tkinter_manager.text_input_manager import TextInputManager
from tkinter_manager.container_manager import ContainerManager
from tkinter_manager.progress_bar_manager import ProgressBarManager
import pytest

@pytest.mark.parametrize(
		"element_name, element_type, label_text, values, expected_elements, expected_type",
		[
			pytest.param('username', 'text_input', 'Username', None, 2, TextInputManager),
			pytest.param('username', 'text_input', None, None, 1, TextInputManager),
			pytest.param('food_order', 'checkboxes', 'Food order', ['Fish', 'Chips', 'Tomato Sauce'], 2, ContainerManager),
			pytest.param('drinks_order', 'radio_buttons', 'Drinks order', ['Tea', 'Coffee', 'Milo'], 2, ContainerManager),
			pytest.param('progress_bar', 'progress_bar', None, None, 1, ProgressBarManager),
		]
)
def test_add_element(element_name, element_type, label_text, values, expected_elements, expected_type):
	manager = TKinterManager("This is the title")
	if values:
		manager.add_element(
			element_name=element_name,
			element_type=element_type,
			label_text=label_text,
			values=values,
		)
	else:
		manager.add_element(
			element_name=element_name,
			element_type=element_type,
			label_text=label_text,
		)
	assert len(manager.elements_dict) == expected_elements
	assert isinstance(manager.get_element(element_name), expected_type)
