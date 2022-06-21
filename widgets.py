"""This contains all the smaller custom widgets that the dialog needs."""

import tkinter

from tkinter import ttk

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