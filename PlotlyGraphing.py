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
        
        def clicked(i):
            chosen.append(buttons[i].objectName())
            buttons[i].setStyleSheet('QPushButton {background-color: #6EA7E7; color: white;}')
            if len(chosen) == 3:
                window.close()

        app, window, layout = self.make_window()
        label = QLabel("Select 3 categories for X, Y, and Z variables")
        layout.addWidget(label)
        chosen = []
        buttons = []
        for i in range(len(self.titles)):
            buttons.append(QPushButton(self.titles[i]))
            
            buttons[i].setObjectName(self.titles[i])
            buttons[i].clicked.connect(lambda _, i=i: clicked(i)) ### always returning last element in list
            #buttons[i].clicked.connect(lambda _, i=i: chosen.append(buttons[i].accessibleName()))
            layout.addWidget(buttons[i])
        
        window.show()
        app.exec_()
        
        
        
        return chosen


    
class Data():
    def __init__(self):
        self.titles = []
        self.chosen = []
        self.points = []
        self.crossed = []
        self.cat = []
        self.d = dict()
        self.jittered = []
        self.collapsedPoints = []
        


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
                ### must work for floats and to discard first line  
                
                if int(row[c_in]) == 1:
                    crossed = 'Crossed'
                else:
                    crossed = 'Not Crossed'
                
                self.points.append([float(row[x_in]), float(row[y_in]), float(row[z_in]), crossed]) 
                    #self.crossed.append(int(row[c_in]))
                ### points in form [x, y, z]
                
    
    def jitter_s(self):     ### returns points evenly distributed on a sphere
        d = self.collapse()
        
        big_x = []
        big_y = []
        big_z = []
        colors = []
        
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
            self.jittered.append([big_x[i], big_y[i], big_z[i]])
        


    def collapseDict(self):
        for i in range(len(self.points)):
            if tuple(self.points[i][:3]) not in self.d:
                if self.points[i][3] == 'Crossed': ### not registering self.
                    self.d[tuple(self.points[i][:3])] = [1, 0]
                else:
                    self.d[tuple(self.points[i][:3])] = [0, 1]
            else:
                if self.points[i][3] == 'Crossed':
                    self.d[tuple(self.points[i][:3])][0] += 1
                else:
                    self.d[tuple(self.points[i][:3])][1] += 1
            
               
        ### dictionary in form {(x, y, z): [# of times crossed, # of times not crossed] of times the point appears}
    
    def collapsePlot(self):
        for key in self.d:
            self.collapsedPoints.append([key[0], key[1], key[2], round(self.d[key][0]/(self.d[key][0] + self.d[key][1]),3)])



    def plot(self, collapsed=False):
        if collapsed:
            df = pd.DataFrame(self.collapsedPoints,  columns=[self.chosen[0],self.chosen[1],self.chosen[2], 'Proportion Crossed'])
            
            fig = px.scatter_3d(df, x=self.chosen[0], y=self.chosen[1], z=self.chosen[2], color='Proportion Crossed')
            fig.update_traces(marker=dict(size=5))
            fig.update_traces(customdata=self.collapsedPoints, selector=dict(type='scatter'))            
            fig.show()    
            ### https://plotly.com/python/reference/scatter/ (hoverinfo)
        else:
            df = pd.DataFrame(self.points,  columns=[self.chosen[0],self.chosen[1],self.chosen[2], 'Crossed'])
            fig = px.scatter_3d(df, x=self.chosen[0], y=self.chosen[1], z=self.chosen[2], color = 'Crossed')
            fig.update_traces(marker=dict(size=5))
            fig.show()

### /Users/willpixley/HVEL/full_file.csv
def main():
    gui = Gui()
    data = Data()
    gui.get_path() ## gets data filepath
    #gui.filepath = '/Users/willpixley/HVEL/full_file.csv'
    gui.titles = data.getTitles(gui.filepath) ### gets and displays column titles
    data.chosen = gui.choose_axes() ## returns selected parameters
    data.make_points(gui.filepath) ### makes point list
    data.collapseDict()
    data.collapsePlot()
    data.plot(collapsed=True)
    

    

if __name__ == '__main__':
    try:
        main()
    except:
        print("Error")



