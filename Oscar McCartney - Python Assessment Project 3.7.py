from tkinter import *
from numpy import sin, cos, tan, sqrt, log10 as log
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
        self.eq_var = StringVar()
        self.eq_var.trace("w", self.draw) # calls self.draw every time self.entry is changed by the user

        self.canvas = Canvas(root, width = 512, height = 512)
        self.canvas.grid(column = 0, columnspan = 2)

        self.canvas.create_line(0, 256, 512, 256) # y-axis line
        self.canvas.create_line(256, 0, 256, 512) # x-axis line

        self.y_label = Label(root, text = "y = ", font = ("Times New Roman Italic", 24))
        self.y_label.grid(row = 2, column = 0)

        self.eq_entry = Entry(root, width = 28, font = ("Times New Roman Italic", 24), textvariable = self.eq_var)
        self.eq_entry.grid(row = 2, column = 1)

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
        
        self.canvas.delete("all")
        self.canvas.create_line(0, 256, 512, 256) # y-axis line
        self.canvas.create_line(256, 0, 256, 512) # x-axis line

        if error_char == "":
            points = []
            self.scale = 32 # one graph unit is equal to 32 screen pixels.
            
            try:
                for x in range(0, 512):
                    points.append(x)
                    x = (x-256)/self.scale # Shifts the y-axis to the middle of the screen and scales the screen so the graph is visible.
                    points.append((eval(eq)) * -self.scale + 256)
                
                if points == [0]:
                    raise error_char
                
                self.canvas.create_line(tuple(points), width = 2, fill = "#000000")
            except Exception as e:
                error_msg = f"{e}"
        else:
            error_msg = f"Invalid character: '{error_char}'"
        
        if error_msg != "invalid syntax (<string>, line 0)": # if self.eq_entry is empty don't display an error.
            self.canvas.create_text(256+self.y_label.winfo_width(), 500, font = 11, fill = "red", text = error_msg)
        self.canvas.update()
        print(error_msg)


if __name__ == "__main__":
    root = Tk()
    root.title(os.path.basename(__file__))
    get_info = GrapherGUI(root)
    root.mainloop()
