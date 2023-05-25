from tkinter import *
from tkinter.ttk import *
from re import *
from numpy import sin, cos, tan
import os

class GrapherGUI:
    """
    A class for the GUI that creates the window and contains all the code for my grapher to function.
    """

    def __init__(self, parent):
        """
        Defines all the variables and widgets that make up the grapher.
        """
        self.eq_var = StringVar()
        self.eq_var.trace("w", self.draw) # calls self.draw every time self.entry is changed by the user

        self.canvas = Canvas(root, width = 512, height = 512)
        self.canvas.grid(column = 0, columnspan = 2)

        x = self.canvas.create_line(0, 256, 512, 256) # x axis line
        y = self.canvas.create_line(256, 0, 256, 512) # y axis line

        self.eq_l = Label(root, text = "y = ", font = ("Times New Roman Italic", 24))
        self.eq_l.grid(row = 1, column = 0, padx = 1)

        self.eq_e = Entry(root, width = 28, font = ("Times New Roman Italic", 24), textvariable = self.eq_var)
        self.eq_e.grid(row = 1, column = 1)

    def draw(self, *args):
        """
        Function that runs every time the entry widget is changed by the user. 
        Validates the equation input and saves the equation to the equation.txt file 
        then draws the graph in the self.canvas Canvas widget.
        """
        self.eq = self.eq_var.get()
        if search("[^ |^x|^(|^)|^-|^+|^*|^**|^sqrt|^sin|^cos|^tan]", self.eq) != None:
            print("error")
        else:
            self.points = []
            self.scale = 32

            for x in range(0, 512):
                self.points.append(x)
                x = (x-256)/self.scale # Shifts the y-axis to the middle of the screen and scales the screen so that sin functions are visible.
                self.points.append((eval(self.eq)) * -self.scale + 256)
            
            self.canvas.create_line(tuple(self.points))
            self.canvas.update()


if __name__ == "__main__":
    root = Tk()
    root.title(os.path.basename(__file__))
    get_info = GrapherGUI(root)
    root.mainloop()
