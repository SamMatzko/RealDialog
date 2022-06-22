"""This contains all the smaller custom widgets that the dialog needs."""

import tkinter

from tkinter import ttk

class PathHistory(ttk.Frame):
    """The widget that shows the path history, and enables users to go back to
    directories that they've already visited."""

    def __init__(self, *args, path, **kwargs):
        super().__init__(*args, **kwargs)
        
        # The path we're showing
        self.path = path

        # The arrow buttons
        self.left_button = tkinter.Button(self, text="<")
        self.left_button.grid(row=0, column=0, sticky="w")

        self.right_button = tkinter.Button(self, text=">")
        self.right_button.grid(row=0, column=2, sticky="e")
        
        # The frame containing the buttons for each step in the path
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.grid(row=0, column=1, sticky="ew")
        
        # The list of path-step buttons
        self.buttons = []
        
        # Show our path
        self.show_path(self.path)
    
    def show_path(self, path):
        """Show the path."""

        # Remove all the old buttons
        for button in self.buttons:
            button.destroy()
        
        # Reset the list of buttons
        self.buttons = []

        # Create the list of path elements we're going to show, limited to six elements
        elements = []
        for element in path.split("/"):
            if element != "":
                elements.append(element)
        elements = elements[-6:]

        # Show the buttons
        for element in elements:
            button = ttk.Button(self.buttons_frame, text=element)
            button.pack(side="left")
            self.buttons.append(button)
        
        # Set our path variable
        self.path = path

class SearchEntry(ttk.Entry):
    """The entry for the search widget. Has some "special" functionality that's
    included in every other text widget on the operating system but is lacking
    in `tkinter` for some stupid reason."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set all the keybindings
        self.bind("<Control-a>", self.select_all)

    def select_all(self, event=None):
        """Select all the text in the entry."""
        self.select_range("0", "end")
        return "break"