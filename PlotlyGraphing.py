import plotly.express as px
import pandas as pd
import csv
import numpy as np
from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import QFont
import sys
from numpy import arange, pi, sin, cos, arccos
# pip install PyQt5
### convert to exe 
# https://guidingcode.com/convert-py-files-to-exe/#:~:text=Using%20cx_freeze%20to%20convert%20.,-py%20file%20to&text=py%20files%20to%20.exe%20is,and%20it%20is%20cross%2Dplatform. 
class Gui():
    def __init__(self):
        self.filepath = ''
        self.titles =[]
        
        
        
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
        app.exec()
        
    
    def choose_axes(self):
        
        def clicked(i):
            chosen.append(buttons[i].objectName())
            buttons[i].setStyleSheet('QPushButton {background-color: #6EA7E7; color: white;}')
            if len(chosen) == 4:
                window.close()

        app, window, layout = self.make_window()
        label = QLabel("Select 3 categories for X, Y, and Z variables. Select a 4th for the gapCrossed column")
        layout.addWidget(label)
        chosen = []
        buttons = []
        self.titles = list(self.titles)
        for i in range(len(self.titles)):
            buttons.append(QPushButton(self.titles[i]))
            buttons[i].setObjectName(self.titles[i])
            buttons[i].clicked.connect(lambda _, i=i: clicked(i)) ### always returning last element in list
            #buttons[i].clicked.connect(lambda _, i=i: chosen.append(buttons[i].accessibleName()))
            layout.addWidget(buttons[i])
        
        window.show()
        app.exec()
        
        
        
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
        self.collapsedPoints = [] ###in form [x, y, z, proportion of gap cross, total gaps for that point, safe or unsafe]
        self.sizes = []
        self.xThresh = 4
        self.yThresh = 4
        self.zThresh = 4
        self.totThresh = 7
        


    def getTitles(self,filename):        ### get column titles
        self.df = pd.read_excel(filename)
        self.df = self.df.to_dict()
        for key in self.df:
            key = key.strip()
        return self.df
        
        
    def make_points(self, filename):
        

        t1 = self.chosen[0]
        t2 = self.chosen[1]
        t3 = self.chosen[2]
        t4 = self.chosen[3]
        xList = self.df[t1]
        yList = self.df[t2]
        zList = self.df[t3]
        cList = self.df[' gapCrossed']
            
        for i in range(len(xList)):
                ### must work for floats and to discard first line  
                
            if int(cList[i]) == 1:
                crossed = 'Crossed'
            else:
                crossed = 'Not Crossed'
                
            self.points.append([float(xList[i]), float(yList[i]), float(zList[i]), crossed]) 
                    #self.crossed.append(int(row[c_in]))
                ### points in form [x, y, z]
                
    
    def jitter_s(self):     ### returns points evenly distributed on a sphere
        d = self.collapseDict()


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
            if key[0] >=self.xThresh and key[1] >= self.yThresh and key[2] >= self.zThresh and (key[0] + key[2]) >= self.totThresh:
                status = "Safe"
            else:
                status = "Not Safe"
            self.collapsedPoints.append([key[0], key[1], key[2], round(self.d[key][0]/(self.d[key][0] + self.d[key][1]),3), sum(self.d[key]), status ])
            self.sizes.append( sum(self.d[key]))






    def plot(self, collapsed=False):
        if collapsed:
            df = pd.DataFrame(self.collapsedPoints,  columns=[self.chosen[0],self.chosen[1],self.chosen[2], 'Proportion Crossed', 'Total Gaps', 'Gap Safety'])
            
            fig = px.scatter_3d(df, x=self.chosen[0], y=self.chosen[1], z=self.chosen[2], color='Proportion Crossed', size='Total Gaps', symbol='Gap Safety')
            #fig.update_traces(marker=dict(size=5))
            fig.update_traces(customdata=self.collapsedPoints, selector=dict(type='scatter')) 
            fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01  ))         
            fig.show()    
            ### https://plotly.com/python/reference/scatter/ (hoverinfo)
        else:
            df = pd.DataFrame(self.points,  columns=[self.chosen[0],self.chosen[1],self.chosen[2], 'Crossed'])
            fig = px.scatter_3d(df, x=self.chosen[0], y=self.chosen[1], z=self.chosen[2], color = 'Crossed')
            #fig.update_traces(marker=dict(self.sizes))
            fig.show()

### /Users/willpixley/HVEL/full_file.csv
def main():
    gui = Gui()
    data = Data()
    #gui.get_path() ## gets data filepath
    gui.filepath = '/Users/willpixley/Downloads/CombinedParticipantsAR.xlsx'
    gui.titles = data.getTitles(gui.filepath) ### gets and displays column titles
    data.chosen = gui.choose_axes() ## returns selected parameters
    data.make_points(gui.filepath) ### makes point list
    data.collapseDict()
    data.collapsePlot()
    data.plot(collapsed=True)
    
    

    

if __name__ == '__main__':
    main()
   



