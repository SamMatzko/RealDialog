"""All the dialogs, made from their base class."""

import glob
import os
import time
import tkinter

from tkinter import ttk

import widgets

class _FileDialog(tkinter.Toplevel):
    """The base class for all the dialogs."""

    def __init__(self, master, action="open", *args, **kwargs):
        super().__init__(*args, master=master, **kwargs)

        # The file/dir that's been selected. None if nothing was selected, or if Cancel was hit.
        self.selected_file = None

        # The user's response (Ok, Cancel)
        self.response = "placeholder"

        # The action this dialog takes (either "open" or "save")
        self.action = action

        # The dialog's parent window
        self.master = master

        # Configure various aspects of the dialog
        self.wm_attributes("-topmost", True)
        self.grab_set()
        self.wm_geometry("900x700+20+20")
        self.wm_protocol("WM_DELETE_WINDOW", self.__cancel)

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

        # Create all the dialog's widgets
        self.__create_widgets()

        # Open the home directory
        self.__show_dir(os.environ["HOME"])

    def __action(self):
        """The dialog's action, either to save or to open."""
        if self.action == "open":
            self.__action_open()
        else:
            self.__action_save()

    def __action_open(self):
        """Submit the file for opening, or just open the directory if a dir is selected."""
        self.selected_file = self.treeview.selection()[0]
        if os.path.isdir(self.selected_file):
            self.__show_dir(self.selected_file)
        else:
            self.response = True

    def __action_save(self):
        """Submit the file for saving, asking first if the user really wants to replace it."""
        self.selected_file = self.treeview.selection()[0]
        self.response = True

    def __cancel(self, event=None):
        """Cancel the dialog."""
        self.response = False

    def __create_widgets(self):
        """Create all the widgets for the file dialog."""

        # The frame for the top buttons
        self.top_button_frame = ttk.Frame(self)
        self.top_button_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.top_button_frame.columnconfigure(0, weight=0)
        self.top_button_frame.columnconfigure(1, weight=1)
        self.top_button_frame.columnconfigure(2, weight=0)
        self.top_button_frame.columnconfigure(3, weight=0)

        # The cancel button
        self.cancel_button = ttk.Button(self.top_button_frame, text="Cancel", underline=0, command=self.__cancel)
        self.cancel_button.grid(row=0, column=0, sticky="w")

        # The search bar
        self.search_bar = ttk.Frame(self.top_button_frame)
        self.search_bar.grid(row=0, column=1, sticky="ew")
        self.search_bar.columnconfigure(0, weight=1)

        # The contents of the search bar
        self.search_entry = widgets.SearchEntry(self.search_bar)
        self.search_entry.grid(row=0, column=0, sticky="ew")
        self.search_entry.grid_remove()

        # The search button, and its state variable
        self.search_button = ttk.Button(self.top_button_frame, text="Search", command=self.__search)
        self.search_button.grid(row=0, column=2, sticky="e")
        self.search_shown = False

        # The action button ("open" in some cases, "save" in others)
        self.action_button = ttk.Button(
            self.top_button_frame,
            text="Open",
            underline=0,
            command=self.__action,
            state="disabled"
        )
        self.action_button.grid(row=0, column=3, sticky="e")

        # The treeview for the files
        self.treeview = ttk.Treeview(self, columns=("size", "modified"))
        self.treeview.bind("<<TreeviewSelect>>", self.__on_select)
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

    def __on_dir_click(self, event=None):
        self.__show_dir(self.treeview.selection()[0])

    def __on_file_click(self, event=None):
        self.selected_file = self.treeview.selection()[0]
        self.response = True

    def __on_select(self, event=None):
        """Handle the event for when an item in the treeview is selected."""

        # If this fails with an IndexError, it means the user double-clicked something.
        try:

            # Set the selected file variable
            self.selected_file = self.treeview.selection()[0]

            # Enable the action button
            self.action_button.config(state="enabled")
        except IndexError:
            pass

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

    def __search(self):
        """The command for the search button, toggling the search entry."""

        # Toggle whether the search bar shows or not
        self.search_shown = not self.search_shown

        # Show or hide the search bar
        if self.search_shown:
            self.search_entry.grid()
            self.search_entry.focus()
        else:
            self.search_entry.grid_remove()

    def __show_dir(self, directory):
        """Display the contents of directory DIRECTORY."""

        # Disable the action button, since nothing will be selected.
        self.action_button.config(state="disabled")

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
                values=(f"{len(os.listdir(d))} item(s)", f"{time.ctime(os.path.getmtime(d))}"),
                tags=("dir")
            )

        # Display the files
        for f in files:
            self.treeview.insert(
                "",
                "end",
                f,
                text=os.path.basename(f),
                image=self.file_image,
                values=(f"{os.path.getsize(f)} bytes", f"{time.ctime(os.path.getmtime(f))}"),
                tags=("file")
            )

        # Configure the event-handling for the files and directories
        self.treeview.tag_bind("dir", "<Double-Button-1>", self.__on_dir_click)
        self.treeview.tag_bind("file", "<Double-Button-1>", self.__on_file_click)

    def show(self):
        """Show the dialog, and return the selected file (if the user hit the action
        button), or None (if the user hit cancel)."""
        while True:
            try:
                self.update()
            except tkinter.TclError:
                break
            if self.response != "placeholder":
                self.destroy()
                break
        if self.response:
            return self.selected_file
        else:
            return None

if __name__ == "__main__":
    # Testing
    root = tkinter.Tk()
    button = tkinter.Button(root, text="_FileDialog", command=lambda: print(_FileDialog(root).show()))
    button.pack()
    ttk.Style().theme_use("classic")
    root.mainloop()