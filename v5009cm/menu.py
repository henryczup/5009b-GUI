# ----- Menu -----
#   Contains a row of labels at the top
#   Mode Selectors
#   Frequency Spinboxes
#   More to come

import tkinter as tk
import tkinter.messagebox


class VMenu(tk.Menu):

    # ----- Constructor -----
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.fileMenu = None
        self.helpMenu = None

        self.fileMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label='File', menu=self.fileMenu)
        self.fileMenu.add_command(label='Exit', command=exit)

        self.helpMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label='Help', menu=self.helpMenu)
        self.helpMenu.add_command(label='About', command=helpAbout)


def helpAbout():
    text = 'Author Peter Mckone\n' \
           'Valon Technology\n' \
           'Sample 5009 GUI code\n' \
           'No Copyright'
    tkinter.messagebox.showinfo('Help About V5009CM', text)
