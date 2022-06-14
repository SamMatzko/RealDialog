"""All the dialogs, made from their base class."""

import glob
import os
import time
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
        self.wm_geometry("900x700+20+20")
        
        # The file and directory images
        FILE_IMAGE = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "res",
            "file.png"
        )
        self.file_image = tkinter.PhotoImage(file=FILE_IMAGE).subsample(4)
        DIR_IMAGE = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "res",
            "dir.png"
        )
        self.dir_image = tkinter.PhotoImage(file=DIR_IMAGE).subsample(4)

        # Create all the dialog's widgets, and set its theme
        self.search_button = ttk.Button(self, text="Search...")
        self.search_button.grid(row=0, column=0, sticky="W")
        style = ttk.Style()
        style.theme_use("clam")
        self.__create_widgets()
        
        # Open the home directory
        self.__show_dir(os.environ["HOME"])
    
    def __create_widgets(self):
        """Create all the widgets for the file dialog."""
        
        # The treeview for the files
        self.treeview = ttk.Treeview(self, columns=("size", "modified"))
        self.treeview.grid(row=1, column=0, sticky="nsew")

        # The scrollbar for the treeview
        self.scrollbar = ttk.Scrollbar(self, command=self.treeview.yview)
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        self.treeview.config(yscrollcommand=self.scrollbar.set)

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
    
    def __open_dir(self, directory):
        """Return two sorted lists (directories, files) of the contents of directory."""
        
        # The lists
        files = []
        dirs = []
        
        # Get the contents of the directory
        contents = os.listdir(directory)
        
        # Sort through the contents
        for c in contents:
            if os.path.isdir(os.path.join(directory, c)):
                dirs.append(os.path.join(directory, c))
            else:
                files.append(os.path.join(directory, c))
        dirs.sort()
        files.sort()
        
        return dirs, files
    
    def __show_dir(self, directory):
        """Display the contents of directory DIRECTORY."""
        
        # Delete all the old rows
        for i in self.treeview.get_children():
            self.treeview.delete(i)
        
        # Get the contents of the directory
        dirs, files = self.__open_dir(directory)
        
        # Display the directories
        for d in dirs:
            self.treeview.insert(
                "",
                "end",
                d + os.path.sep,
                text=os.path.basename(d),
                image=self.dir_image,
                values=(f"{len(os.listdir(d))} item(s)", f"{time.ctime(os.path.getmtime(d))}")
            )

        # Display the files
        for f in files:
            self.treeview.insert(
                "",
                "end",
                f,
                text=os.path.basename(f),
                image=self.file_image,
                values=(f"{os.path.getsize(f)} bytes", f"{time.ctime(os.path.getmtime(f))}")
            )

if __name__ == "__main__":
    # Testing
    root = tkinter.Tk()
    button = tkinter.Button(root, text="_FileDialog", command=lambda: _FileDialog(root))
    button.pack()
    ttk.Style().theme_use("classic")
    root.mainloop()