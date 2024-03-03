# TKinter Manager
Need a GUI quickly? The TKinter Manager can help, reducing the amount of time you have to spend writing boilerplate code.

## Installation
Clone the repo - no extra libraries needed.

## Usage
To create a new TKinter Manager instance:
```
from tkinter_manager import TKinterManager
manager = TKinterManager(
    title="This is the title"
)
```

To add an element (also known as [widgets in TKinter](https://www.geeksforgeeks.org/what-are-widgets-in-tkinter/))
```
manager.add_element(
	element_name='category',
	element_type='dropdown',
    values=['A', 'B', 'C']
)
```

### Types of TKinter Manager Elements

**Singular Elements**

Button
```
manager.add_element(
	element_name='start_button',
	element_type='button',
	hook_function=app.execute
)
```

Dropdown
```
manager.add_element(
	element_name='category',
	element_type='dropdown',
    values=['A', 'B', 'C']
)
```

Label
```
manager.add_element(
	element_name='message_box',
	element_type='label',
)
```

Progress Bar
```
manager.add_element(
	element_name='progress_bar',
	element_type='progress_bar',
)
```

Text Input
```
manager.add_element(
	element_name='username',
	element_type='text_input',
)
```

**Grouped Elements**  

Checkboxes
```
manager.add_element(
	element_name='food_order',
	element_type='checkboxes',
	values=['Fish', 'Chips', 'Tomato Sauce']
)
```

Radio Buttons
```
manager.add_element(
	element_name='drinks_order',
	element_type='radio_buttons',
    values=['Tea', 'Coffee', 'Milo']
)
```

### Adding labels
To add an element, specify the `label_text` argument.

```
manager.add_element(
	element_name='username',
	element_type='text_input',
	label_text='Enter a username:'
)
```

![Adding a label to an element](img/label_text.jpg)

### Accessing an element
To access an element, use the `manager.get_element()` method:
```
name = "notes"
manager.add_element(
	element_name=name,
	element_type='text_input'
)
name_element = manager.get_element(name)
```

Automatically-added labels can be accessed with the parent element name + "\_label".
```
name = "progress_bar"
manager.add_element(
	element_name=name,
	element_type='progress_bar',
    label_text='Progress so far...'
)
progress_bar_label = manager.get_element(f"{name}_label")
```


### Setting the layout
To centre all added elements, use the `manager.centre_elements()` method. This also makes the elements reactive when resizing the window.

```
manager = TKinterManager("This is the title")
manager.add_element(
	element_name='category',
	element_type='dropdown',
	label_text='Category'
    values=['A', 'B', 'C']
)
manager.add_element(
	element_name='username',
	element_type='text_input',
	label_text='Username'
)
manager.add_element(
	element_name='notes',
	element_type='text_input',
	label_text='Enter notes'
)
manager.add_element(
	element_name='start_button',
	element_type='button',
	hook_function=app.execute
)
manager.centre_elements()
manager.run()
```

![Centring all elements](img/example_centred.jpg)

To explicitly specify an element's place in a grid, use the `manager.set_layout(layout_schema)` method. The input must be a 2D array.

```
manager = TKinterManager("This is the title")
manager.add_element(
	element_name='category',
	element_type='dropdown',
	label_test='Category',
    values=['A', 'B', 'C']
)
manager.add_element(
	element_name='username',
	element_type='text_input',
	label_test='Username',
)
manager.add_element(
	element_name='notes',
	element_type='text_input',
	label_text='Enter notes'
)
manager.add_element(
	element_name='start_button',
	element_type='button',
	hook_function=app.execute
)
layout = [
    ["category_label", "category",],
    ["username_label", "username"],
    ["notes_label", "notes"],
    [None, "start_button"],
]
manager.set_layout(layout)
manager.run()
```

![Explicitly setting a layout](img/set_layout.jpg)

### Element names
When naming elements, the only limitation is that each element must have a unique name. While you can name them anything, it is recommended that a `snake_case` naming style is used.

## Full example
See [the full example code](/examples/full.py) to test it out.  

![Example code output](img/example_code.jpg)