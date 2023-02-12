import plotly.express as px
import pandas as pd
import csv
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QFont
import sys
from numpy import arange, pi, sin, cos, arccos
# pip install PyQt5
### convert to exe 
# https://guidingcode.com/convert-py-files-to-exe/#:~:text=Using%20cx_freeze%20to%20convert%20.,-py%20file%20to&text=py%20files%20to%20.exe%20is,and%20it%20is%20cross%2Dplatform. 
class Gui():
    def __init__(self):
        self.filepath = ''
        self.titles =['yes', 'no', '5', '6']
        
        
    def onClick(self, msg, window):
        self.filepath = msg
        window.close()

    
    def make_window(self):      ### makes base window, returns app, window, layout for future use
        app = QApplication(sys.argv)
        window = QWidget()
        layout = QVBoxLayout()
        window.setLayout(layout)
        return app, window, layout

    def get_path(self):    
        app = QApplication(sys.argv)
        
        window = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Enter filepath") 
        textbox = QTextEdit()
        button = QPushButton("Submit")
        layout.addWidget(label)
        layout.addWidget(textbox)
        layout.addWidget(button)
        
        button.clicked.connect(lambda: self.onClick(textbox.toPlainText(), window))
        window.setLayout(layout)
        window.show()
        app.exec_()
        
    
    def choose_axes(self):
        
        app, window, layout = self.make_window()
        label = QLabel("Select 3 categories for X, Y, and Z variables")
        layout.addWidget(label)
        chosen = []
        buttons = []
        for i in range(len(self.titles)):
            buttons.append(QPushButton(self.titles[i]))
            buttons[i].setAccessibleName(self.titles[i])
            buttons[i].clicked.connect(lambda _, i=i: chosen.append(buttons[i].accessibleName())) ### always returning last element in list
            layout.addWidget(buttons[i])
        
        window.show()
        app.exec_()
        window.close()
        return chosen


    
class Data():
    def __init__(self):
        self.titles = []
        self.chosen = []
        self.points = []
        self.crossed = []
        self.cat = []


    def getTitles(self,filename):        ### get column titles
        with open(filename, 'r') as file:     # open file
            n_file = csv.reader(file)
            for row in n_file:
                self.titles.append(row)
                break
        return self.titles[0]

    def make_points(self, filename):
        with open(filename, 'r') as file:     # open file
            n_file = csv.reader(file)
            columns = []
            for row in n_file:
                for i in range(len(row)):
                    columns.append(row[i].strip())
                break
            x_in = columns.index(self.chosen[0])
            y_in = columns.index(self.chosen[1])
            z_in = columns.index(self.chosen[2])
            c_in = columns.index('gapCrossed')
            for row in n_file:
                try:
                    self.points.append([int(row[x_in]), int(row[y_in]), int(row[z_in]), row[c_in]]) 
                    #self.crossed.append(int(row[c_in]))
                ### points in form [x, y, z]
                except:
                    continue
    
    def jitter_s(self):     ### returns points evenly distributed on a sphere
        d = self.collapse()
        
        big_x = []
        big_y = []
        big_z = []
        colors = []
        full = []
        for key in d:    
            n = d[key]
            
            i = arange(0, n, dtype=float) + 0.025
            phi = arccos(1 - 2*i/n)
            goldenRatio = (1 + 5**0.5)/2
            theta = 2 * pi * i / goldenRatio
            x, y, z = cos(theta) * sin(phi), sin(theta) * sin(phi), cos(phi)
            colors.extend(d[key])
            for j in range(len(x)):
                
                x[j] = x[j] + int(key[0])
                y[j] = y[j] + int(key[1])
                z[j] = z[j] + int(key[2])
        for i in range(len(big_x)):
            full.append([big_x[i], big_y[i], big_z[i]])
        return full


    def collapse(self):
        d = dict()
        for i in range(len(self.points)):
            if self.points[i] not in d:
                d[self.points[i]] = 0
            else:
                d[self.points[i]] += 1
        ### dictionary in form {[x, y, z]: [1, 0, 1, 0, 0]}
        return d

    def plot(self):
        df = pd.DataFrame(self.points,  columns=['x','y','z', 'Categories'])
        print(df)
        fig = px.scatter_3d(df, x='x', y='y', z='z')
        fig.update_traces(marker=dict(size=5))
        fig.show()

### /Users/willpixley/HVEL/full_file.csv
def main():
    gui = Gui()
    data = Data()
    gui.get_path() ## gets data filepath
    
    gui.titles = data.getTitles(gui.filepath) ### gets and displays column titles
    data.chosen = gui.choose_axes() ## returns selected parameters
    data.make_points(gui.filepath) ### makes point list
    print(data.points)
    data.plot()
    

    

main()


