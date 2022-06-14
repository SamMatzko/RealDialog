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
        
        # Set the dialog's size
        self.wm_attributes("-zoomed", True)
        
        # Create all the dialog's widgets, and set its theme
        self.search_button = ttk.Button(self, text="Search...")
        self.search_button.grid(row=0, column=0, sticky="W")
        style = ttk.Style()
        style.theme_use("clam")
        self.__create_widgets()
    
    def __create_widgets(self):
        """Create all the widgets for the file dialog."""
        
        # The treeview for the files
        self.treeview = ttk.Treeview(self, columns=("size", "modified"))
        self.treeview.grid(row=1, column=0, sticky="NSEW")

        # The name column
        self.treeview.heading("#0", text="Name")
        self.treeview.column("#0", anchor="w", minwidth=200)

        # The size column
        self.treeview.heading("size", text="Size")
        self.treeview.column("size", anchor="w", minwidth=100)

        # The modified column
        self.treeview.heading("modified", text="Modified")
        self.treeview.column("modified", anchor="w", minwidth=300)

        # Set the rows' and columns' stretchability
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
    
    def __open_dir(self, dir):
        """Display the contents of directory DIR."""
        
        # Delete all the old rows
        for i in self.treeview.get_children():
            self.treeview.delete(i)

if __name__ == "__main__":
    # Testing
    root = tkinter.Tk()
    button = tkinter.Button(root, text="_FileDialog", command=lambda: _FileDialog(root))
    button.pack()
    ttk.Style().theme_use("classic")
    root.mainloop()