from tkinter import *
from tkinter.ttk import *
import os

class GrapherGUI:
    """
    A class for the GUI that creates the window and contains all the code for my grapher to function.
    """

    def __init__(self, parent):
        """
        Defines all the variables and widgets that make up the grapher.
        """

        self.canvas = Canvas(root, width = 512, height = 512)
        x = self.canvas.create_line(0, 256, 512, 256)
        y = self.canvas.create_line(256, 0, 256, 512)
        self.canvas.grid()

        self.entry = Entry(root, width = 32, font = ("Times New Roman Italic", 24), )
        self.entry.grid(row = 1)


if __name__ == "__main__":
    root = Tk()
    root.title(os.path.basename(__file__))
    get_info = GrapherGUI(root)
    root.mainloop()
