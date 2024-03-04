import os
import tkinter as tk
import platform


class ContextMenuWidget(tk.Menu):
    """Extended widget with a context menu that includes Cut, Copy, and Paste commands."""

    ICON_PATH = os.path.join(os.path.dirname(__file__), "Assets/Images")

    ICONS = {
        "Cut": "edit-cut.png",
        "Copy": "edit-copy.png",
        "Paste": "edit-paste.png",
    }

    def __init__(self, widget: tk.Widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = widget
        self.config(tearoff=False)

        self.icons = {}
        for label, icon_file in self.ICONS.items():
            icon_path = os.path.join(self.ICON_PATH, icon_file)
            self.icons[label] = tk.PhotoImage(file=icon_path)

            self.add_command(
                label=label,
                image=self.icons[label],
                compound="left",
                accelerator=self.get_accelerator(label),
                command=self.get_command(label)
            )

        self.add_separator()
        self.add_command(
            label="Select all",
            accelerator="Ctrl+A",
            command=self.on_select_all
        )

        self.map_right_button_event()

        self.widget.bind("<<RightClick>>", self.show_menu)
        self.widget.bind("<Control-a>", self.on_select_all)
        self.widget.bind("<Control-A>", self.on_select_all)

    def map_right_button_event(self):
        if platform.system() == "Darwin":
            self.event_add("<<RightClick>>", "<Button-2>")
        else:
            self.event_add("<<RightClick>>", "<Button-3>")

    def update_menu_state(self):
        try:
            if isinstance(self.widget, tk.Text):
                widget_content = self.widget.get("1.0", tk.END).strip()
            else:
                widget_content = self.widget.get()
        except AttributeError as error:
            print(error)
            return False

        try:
            clipboard_content = self.widget.clipboard_get()
        except tk.TclError:
            clipboard_content = ""

        content_available = bool(widget_content)

        for label in self.ICONS.keys():
            self.entryconfig(
                label,
                state="normal" if content_available else "disabled"
            )

        self.entryconfig(
            "Paste",
            state="normal" if clipboard_content else "disabled"
        )

        return True

    def on_cut(self):
        self.widget.event_generate("<<Cut>>")

    def on_copy(self):
        self.widget.event_generate("<<Copy>>")

    def on_paste(self):
        self.widget.event_generate("<<Paste>>")

    def show_menu(self, event=None):
        if self.update_menu_state():
            self.tk_popup(event.x_root, event.y_root)

    def on_select_all(self, event=None):
        self.widget.event_generate("<<SelectAll>>")
        return "break"

    def get_accelerator(self, label):
        if platform.system() == "Darwin":
            if label == "Cut":
                return "Command+X"
            elif label == "Copy":
                return "Command+C"
            else:
                return "Command+V"
        else:
            if label == "Cut":
                return "Ctrl+X"
            elif label == "Copy":
                return "Ctrl+C"
            else:
                return "Ctrl+V"

    def get_command(self, label):
        if label == "Cut":
            return self.on_cut
        elif label == "Copy":
            return self.on_copy
        elif label == "Paste":
            return self.on_paste
        else:
            return None
