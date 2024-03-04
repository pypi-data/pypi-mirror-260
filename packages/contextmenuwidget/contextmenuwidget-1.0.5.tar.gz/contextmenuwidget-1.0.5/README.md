# context_menu_widget

[![PyPI version](https://badge.fury.io/py/ContextMenuWidget.svg)](https://badge.fury.io/py/ContextMenuWidget)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Description

ContextMenuWidget is a Python package that provides an extended `tk.Menu` class with a context menu for specified widgets, including commands like Cut, Copy, Paste, and Select All.

## Installation

Install the package using pip:

```bash
pip install ContextMenuWidget
```
## Usage
from contextmenuwidget import ContextMenuWidget

## Current version : V1.0.5

## Release Notes

### Version 1.0.5 (March 03, 2024)
- Fixed a bug related to displaying shortcut (MacOS)


# Example usage of the ContextMenuWidget class

```python
from contextmenuwidget import ContextMenuWidget

root = tk.Tk()

label_entry = tk.Label(root, text="Entry Widget : ")
label_entry.grid(column=0, row=0, sticky="w")

widget_entry = tk.Entry(root, width=31)
widget_entry.grid(column=1, row=0, sticky="w")
context_menu = ContextMenuWidget(widget_entry)

label_text = tk.Label(root, text="Text Widget : ")
label_text.grid(column=0, row=1, sticky="wn")

widget_text = tk.Text(root, height=13, width=31, wrap=tk.NONE)
widget_text.grid(column=1, row=1, sticky="w")
context_menu = ContextMenuWidget(widget_text)

vertical_scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
vertical_scrollbar.grid(column=2, row=1, sticky="ns")
widget_text.config(yscrollcommand=vertical_scrollbar.set)
vertical_scrollbar.config(command=widget_text.yview)

horizontal_scrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL)
horizontal_scrollbar.grid(column=1, row=2, sticky="we")
widget_text.config(xscrollcommand=horizontal_scrollbar.set)
horizontal_scrollbar.config(command=widget_text.xview)

root.mainloop()
```

## Features
Context Menu: Extends tk.Menu with Cut, Copy, Paste, and Select All commands.
Icons: Utilizes icons for visual representation of menu commands.
Dynamic Updates: Dynamically updates menu entry states based on widget content and clipboard status.
Cross-Platform: Supports right-click events on different platforms.

## Dependencies
tkinter (Ensure that tkinter is installed)

## License
This project is licensed under the MIT License - see the LICENSE file for details.