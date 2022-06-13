"""All the dialogs, made from their base class."""

import glob
import tkinter

from tkinter import ttk

class _FileDialog(tkinter.Toplevel):
    """The base class for all the dialogs."""
    
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, master=master, **kwargs)
        
        # The dialog's parent window
        self.master = master

        # Set the dialog to be modal
        self.wm_attributes("-topmost", True)
        self.grab_set()
        
        # Create all the dialog's widgets, and set its theme
        self.search_button = ttk.Button(self, text="Search...")
        self.search_button.pack()
        style = ttk.Style()
        style.theme_use("clam")