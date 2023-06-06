from tkinter import *
from numpy import sin, cos, tan, sqrt, log10 as log, nan, inf
import numpy as np
import re
import os

class GrapherGUI:
    """
    A class for the GUI that creates the window and contains all the code for my grapher to function.
    """

    def __init__(self, parent):
        """
        Defines all the variables and widgets that make up the grapher.
        """
        np.seterr(divide = 'ignore') # stops divide by 0 errors
        self.scale = 32 # one graph unit is equal to this many screen pixels.
        self.num_period = 5*self.scale # the period (in pixels) in between the numbers on the x and y axis

        self.eq_var = StringVar()
        self.eq_var.trace("w", self.draw) # calls self.draw every time self.entry is changed by the user

        self.canvas = Canvas(root, width = 512, height = 512)
        self.canvas.grid(column = 0, columnspan = 2)

        self.y_label = Label(root, text = "y = ", font = ("Times New Roman Italic", 24))
        self.y_label.grid(row = 2, column = 0)

        self.eq_entry = Entry(root, width = 28, font = ("Times New Roman Italic", 24), textvariable = self.eq_var)
        self.eq_entry.grid(row = 2, column = 1)
        
        self.canvas_reset()

    def draw(self, *args):
        """
        Function that runs every time the entry widget is changed by the user. 
        Validates the equation input and saves the equation to the equation.txt file 
        then draws the graph in the self.canvas Canvas widget.
        """
        eq = self.eq_var.get()
        error_msg = ""
        error_char = ""
        eq_list = [x for x in eq] # a list of all the characters in eq where each item is one character long
        eq_valid = [x for x in "".join(re.findall(r"[x+\-*/() .]|\d|\*\*|sqrt\(|sin\(|cos\(|tan\(|log\(", eq))] # a list of all the valid characters in eq
        for x in range(len(eq_list)): # compares each item of eq_list and eq_valid and if they are different it assigns the different item to error_char
            real = eq_list[x]
            try:
                valid = eq_valid[x]
            except:
                error_char = real
                break
            if real != valid:
                error_char = real
                break
        
        self.canvas_reset()

        if error_char == "":
            points = []
            
            try:
                for i in range(0, 512):
                    points.append([i])
                    x = ((i)-256)/self.scale # Shifts the y-axis to the middle of the screen and scales the screen so the graph is visible.
                    y = (eval(eq)) * -self.scale + 256
                    points[i].append(y)
                
                points = [x for x in points if x[1] == x[1] and abs(x[1]) != inf] # any expression involving nan is autmatically False so the only way to check for nan is to check if x[1] is equal to itself.
                self.canvas.create_line(tuple(points), width = 2, fill = "#000000")

            except Exception as e:
                error_msg = str(e).split('(<')[0]
        
        else:
            error_msg = f"Error at character: '{error_char}'"
        
        if eq != "": # if eq is empty don't display an error.
            self.canvas.create_text(256+self.y_label.winfo_width(), 500, font = 11, fill = "red", text = error_msg)
            self.canvas.update()

    def canvas_reset(self):
        """
        Clears the canvas and draws the axis lines.
        """
        start = -((self.num_period)-(256%(self.num_period))) # x/y coordinate at which the axis lines will start to be drawn
        self.canvas.delete("all")

        for x in range(start, 512-start, self.scale):
            self.canvas.create_line(x, 0, x, 512, fill = "#D0D0D0")
        
        for y in range(start, 512-start, self.scale):
            self.canvas.create_line(0, y, 512, y, fill = "#D0D0D0")

        for x in range(start, 512-start, self.num_period):
            self.canvas.create_line(x, 0, x, 512, fill = "#A0A0A0")
            x_disp = int((256-x)/-self.scale)
            if x_disp != 0:
                self.canvas.create_text(x, 270, text = x_disp, font = ("Times New Roman", 14))
        
        for y in range(start, 512-start, self.num_period):
            self.canvas.create_line(0, y, 512, y, fill = "#A0A0A0")
            y_disp = int((256-y)/self.scale)
            if y_disp != 0:
                self.canvas.create_text(242, y, text = y_disp, font = ("Times New Roman", 14))

        self.canvas.create_text(242, 270, text = "0", font = ("Times New Roman", 14))
        self.canvas.create_line(0, 256, 512, 256)
        self.canvas.create_line(256, 0, 256, 512)


if __name__ == "__main__":
    root = Tk()
    root.title(os.path.basename(__file__))
    get_info = GrapherGUI(root)
    root.mainloop()
