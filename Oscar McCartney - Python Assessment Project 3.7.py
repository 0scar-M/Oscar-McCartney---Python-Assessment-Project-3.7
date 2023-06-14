from tkinter import *
from tkinter import ttk
from numpy import sin, cos, tan, sqrt, log10 as log, nan, inf
import numpy as np
import re
import os

class GrapherGUI:
    """
    A class for the GUI that creates the window and contains all the code for the grapher to function.
    """

    def __init__(self, parent):
        """
        Defines all the variables and widgets that make up the grapher.
        """
        np.seterr(divide = "ignore") # stops divide by 0 and log -ve number errors
        root.bind("<MouseWheel>", self.mouse_zoom)
        self.EQ_FILE = os.path.join(os.path.dirname(__file__), "equation.txt")

        self.points = [] # the points to be plotted on the graph
        self.scale = 32 # one graph unit is equal to this many screen pixels.
        self.num_period = 5 # how often a number is drawn on the x or y axis in graph units
        self.num_period_pixels = self.num_period*self.scale # how often a number is drawn on the graph in pixels
        self.zoom_points = [[640, 0.1], [256, 0.2], [128, 0.5], [64, 1], [25, 2], [13, 5], [6.5, 10], [2.5, 20], [0.15, 50], [0, 50]] # a list of self.scale values at which the graph needs to change self.num_period so that the numbers on the x and y axis are readable and the corresponding self.num_period value to change it to.

        self.style = ttk.Style() # style for the zoom in and zoom out buttons. I chose to use ttk buttons for the zoom in and out because they look really good with the regular tkinter.Scale widget.
        self.style.configure("ZIO.TButton", font = ("Courier", 11)) # Courier is a monospace font so - and + have the same width which makes it easy to get the width of the buttons right.
    
        self.eq_var = StringVar()
        self.eq_var.trace("w", self.draw) # calls self.draw every time self.entry is changed by the user

        self.canvas = Canvas(parent, width = 512, height = 512)
        self.canvas.grid(row = 0, rowspan = 3, column = 0, columnspan = 2)

        self.y_label = ttk.Label(parent, text = "y = ", font = ("Times New Roman Italic", 24))
        self.y_label.grid(row = 3, column = 0)

        self.eq_entry = Entry(parent, width = 29, font = ("Times New Roman Italic", 24), textvariable = self.eq_var)
        self.eq_entry.grid(row = 3, column = 1, columnspan = 2, sticky = W)

        self.zoom_in_button = ttk.Button(parent, text = "+", width = 0, style = "ZIO.TButton", command = self.zoom_in)
        self.zoom_in_button.grid(row = 0, column = 2, sticky = S)

        self.zoom = Scale(parent, from_ = 2.05, to = 0.05, resolution = 0.001, orient = VERTICAL, showvalue = 0, length = 440, command = self.draw)
        self.zoom.set(1.0)
        self.zoom.grid(row = 1, column = 2)

        self.zoom_out_button = ttk.Button(parent, text = "-", width = 0, style = "ZIO.TButton", command = self.zoom_out)
        self.zoom_out_button.grid(row = 2, column = 2, sticky = N)
        
        try: # if equation.txt doesn't exist create it
            open(self.EQ_FILE, "x")
        except:
            self.eq_entry.insert(0, open(self.EQ_FILE, "r+").read())
        self.eq = self.eq_entry.get() # the equation to be drawn

        self.draw()

    def draw(self, *args):
        """
        Runs every time self.eq_entry or self.zoom are changed. 
        Validates the equation input, saves the equation to the equation.txt file and draws the graph.
        """
        self.eq = self.eq_var.get()
        self.num_period_pixels = self.num_period*self.scale
        with open(self.EQ_FILE, "w") as file:
            file.write(self.eq)

        if len(args) == 1:
            self.scale = 32*20**(float(args[0])-1) # if self.zoom was changed then update self.scale to match
            self.num_period = [x[1] for x in self.zoom_points if x[0] <= self.scale][0] # changes the spacing of the numbers on the x and y axes            
        
        error_msg = ""
        eq_list = [str(x) for x in self.eq] # a list of all the characters in self.eq where each item is one character long
        eq_valid_list = [str(x) for x in "".join(re.findall(r"[x+\-*/() .]|\d|\*\*|sqrt\(|sin\(|cos\(|tan\(|log\(", self.eq))] # a list of all the valid characters in self.eq
        try:
            error_char = eq_list[list(np.compare_chararrays(eq_list, (eq_valid_list+["" for _ in range(abs(len(eq_valid_list)-len(eq_list)))]), "==", False)).index(False)] # finds the first character in eq_list that isn't valid
        except:
            error_char = ""

        self.canvas_reset()

        if error_char == "":
            self.points = []
            
            try:
                for i in range(0, 512):
                    self.points.append([i])
                    x = ((i)-256)/self.scale # Shifts the y-axis to the middle of the screen and scales the screen.
                    y = (eval(self.eq)) * -self.scale + 256
                    if y < 0: y = 0 # if y gets too small then tkinter can't draw the line so this just caps y at 0.
                    self.points[i].append(y)
                
                self.points = [[x[0], 512] if abs(x[1]) == inf else x for x in [x for x in self.points if x[1] == x[1]]] # any expression involving nan is autmatically False so the only way to check for nan is to check if x[1] is equal to itself.
                if "log" in self.eq: # makes sure that the asymptote for log graphs is drawn because my grapher doesn't calculate every y value, only 512.
                    self.points[0][1] = 512
                self.canvas.create_line(tuple(self.points), width = 2, fill = "#000000")

            except Exception as e:
                error_msg = str(e).split('(<')[0]
        else:
            error_msg = f"Error at character: '{error_char}'"

        if self.eq != "": # if self.eq is empty don't display an error.
            self.canvas.create_text(256+self.y_label.winfo_width(), 500, font = 11, fill = "red", text = error_msg)
        
        self.canvas.update()

    def canvas_reset(self):
        """
        Clears the canvas and draws the axis lines.
        """
        self.num_period_pixels = self.num_period*self.scale
        start = 256-(np.ceil(256/self.num_period_pixels)*self.num_period_pixels) # x/y coordinate at which the axis lines will start to be drawn
        self.canvas.delete("all")

        for x in np.arange(start, 512-start, self.scale*self.num_period/5): # np.arange allows the for loop to increment by a float.
            self.canvas.create_line(x, 0, x, 512, fill = "#D0D0D0")
        
        for y in np.arange(start, 512-start, self.scale*self.num_period/5):
            self.canvas.create_line(0, y, 512, y, fill = "#D0D0D0")

        for x in np.arange(start, 512-start, self.num_period_pixels):
            self.canvas.create_line(x, 0, x, 512, fill = "#A0A0A0")
            x_disp = float("%.7g" % ((256-x)/-self.scale))
            if str(x_disp).split(".")[1] == "0": x_disp = int(x_disp) # turns x_disp into an int if it ends in .0
            if x_disp != 0:
                self.canvas.create_text(x, 270, text = x_disp, font = ("Times New Roman", 14))
        
        for y in np.arange(start, 512-start, self.num_period_pixels):
            self.canvas.create_line(0, y, 512, y, fill = "#A0A0A0")
            y_disp = float("%.7g" % ((y-256)/-self.scale))
            if str(y_disp).split(".")[1] == "0": y_disp = int(y_disp) # turns y_disp into an int if it ends in .0
            if y_disp != 0:
                self.canvas.create_text(242, y, text = y_disp, font = ("Times New Roman", 14))

        self.canvas.create_text(242, 270, text = "0", font = ("Times New Roman", 14))
        self.canvas.create_line(0, 256, 512, 256)
        self.canvas.create_line(256, 0, 256, 512)

    def zoom_in(self):
        """
        Zooms in by 0.1 everytime the + button is pressed.
        """
        self.zoom.set(self.zoom.get()+0.1)
    
    def zoom_out(self):
        """
        Zooms out by 0.1 everytime the - button is pressed.
        """
        self.zoom.set(self.zoom.get()-0.1)
    
    def mouse_zoom(self, event):
        """
        Zooms in or out by event.delta/2500 every time the scroll wheel is moved.
        """
        self.zoom.set(self.zoom.get()+event.delta/2500) # if scroll down then event.delta = -120 but if scroll up then event.delta = 120


if __name__ == "__main__":
    root = Tk()
    root.title(os.path.basename(__file__))
    get_info = GrapherGUI(root)
    root.mainloop()
