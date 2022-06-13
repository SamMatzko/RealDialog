"""Tests the functionality of the file dialog."""

import tkinter
from tkinter import ttk

from dialogs import _FileDialog

root = tkinter.Tk()
button = tkinter.Button(root, text="_FileDialog", command=lambda: _FileDialog(root))
button.pack()
ttk.Style().theme_use("classic")
root.mainloop()