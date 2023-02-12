### make interactive https://matplotlib.org/stable/users/explain/interactive.html 
### https://matplotlib.org/stable/users/explain/event_handling.html# 

def main():
    import csv
    from mpl_toolkits import mplot3d
    import numpy as np
    import matplotlib.pyplot as plt
    from collections import Counter
    import random
    from numpy import arange, pi, sin, cos, arccos

    

    def make_points(filename): ## returns a list of lists of points
        '''
        x_cat = input('Which x value do you want to look at?\n')
        x_thresh = float(input('Enter threshold for '+x_cat+"\n"))
        y_cat = input('Which y value do you want to look at?\n')
        y_thresh = float(input('Enter threshold for '+y_cat+"\n"))
        z_cat = input('Which z value do you want to look at?\n')
        z_thresh = float(input('Enter threshold for '+z_cat+"\n"))
        '''

        x_cat = 'nearLaneGap'
        x_thresh = 4.0
        y_cat = 'farLaneGap'
        y_thresh = 4.0
        z_cat = 'Overlap'
        z_thresh = 4.0

        ax.set_xlabel(x_cat, fontweight = 'bold')
        ax.set_ylabel(y_cat, fontweight = 'bold')
        ax.set_zlabel(z_cat, fontweight = 'bold')
        points = []
        crossed = []

        with open(filename, 'r') as file:     # open file
            n_file = csv.reader(file)
            columns = []
            for row in n_file:
                for i in range(len(row)):
                    columns.append(row[i].strip())
                break
            x_in = columns.index(x_cat)
            y_in = columns.index(y_cat)
            z_in = columns.index(z_cat)
            c_in = columns.index('gapCrossed')
            
            for row in n_file:
                crossed.append(row[c_in])
                points.append([(row[x_in], row[y_in], row[z_in])]) 
                ##points is a list of lists in form (x, y, z)
            del points[0], crossed[0]  
        
        return points, x_thresh, y_thresh, z_thresh, crossed
    
    def color(points, tx, ty, tz, crossed, tt=6):
        
        
        for i in range(len(points)):
            if int(points[i][0][0])>tx and int(points[i][0][1])>ty and int(points[i][0][2])>tz and int(points[i][0][0])+float(points[i][0][2]) > tt:
                if int(crossed[i]) == 1:
                    points[i].append('Crossed Safe Gap')
                else:
                    points[i].append('Passed Safe Gap')
            else:
                if int(crossed[i]) == 1:
                    points[i].append('Crossed Unsafe Gap')
                else:
                    points[i].append('Passed Unsafe Gap')
    

    def alert_zone(x, y, z, t_x, t_y, t_z):
        a, b, c = np.indices((int(max(x)), int(max(y)), int(max(z))))
        cube2 = (a >= t_x+1) & (b >= t_y+1) & (c >= t_z+1)
        voxels = cube2
        # set the colors of each object
        colors = np.empty(voxels.shape, dtype=object)
        colors[cube2] = 'green'
        # and plot everything
        ax.voxels(voxels, facecolors=colors, alpha = .3)
  
        
        
    def collapse(points):
        d = dict()
        
        
        for i in range(len(points)):
            
            if points[i][0] not in d:
                d[points[i][0]] = [points[i][1]]
            else:
                d[points[i][0]].append(points[i][1])
        return d
        
    #http://extremelearning.com.au/evenly-distributing-points-on-a-sphere/
    def jitter(points, d):       ###need to iterate over dictionary d, containg all the points in { (3, 2, 1): [green, red, blue]}
        big_x = []
        big_y = []
        big_z = []
        colors = []
        for key in d:    
            n = len(d[key])
            
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
            big_x.extend(x)
            big_y.extend(y)
            big_z.extend(z)
        return big_x, big_y, big_z, colors

    def readable(x,y,z,colors):
        p_list = []
        s_list = []
        for i in range(len(x)):
            p_list.append([x[i],y[i],z[i],colors[i]])
            
        return p_list

    def read_d(d):
        p = []
        for key in d:
            if len(d[key]) > 1:
                p.append([key, 'pink'])
            else:
                p.append([key, 'blue'])
        return p
    
    filename = '/Users/willpixley/Downloads/Combined AR Pilot2all for graphing.csv'
    fig = plt.figure(figsize = (8, 8))
    ax = plt.axes(projection ='3d')
    points, x_thresh, y_thresh, z_thresh, crossed = make_points('/Users/willpixley/Downloads/Combined AR Pilot2all for graphing.csv')
    color(points, x_thresh, y_thresh, z_thresh, crossed)

    d = collapse(points)

    

    
    
    x, y, z, colors = jitter(points, d)
    p = readable(x,y,z,colors)
    #p = read_d(d)


    #alert_zone(x, y, z, x_thresh, y_thresh, z_thresh)
    '''
    for key in d:

        #plt.rcParams["figure.figsize"] = [7.00, 3.50]
        plt.rcParams["figure.autolayout"] = True
        #fig = plt.figure()
        #ax = fig.add_subplot(projection='3d')
        r = 0.05
        u, v = np.mgrid[0:2 * np.pi:30j, 0:np.pi:20j]       #2, 30, 20
        x1 = (np.cos(u) * np.sin(v)) 
        print(x1)
        y1 = (np.sin(u) * np.sin(v)) 
        z1 = np.cos(v) 
        for i in range(len(x1)):
            x1[i] = x[i] + key[0]
            y1[i] = y[i] + key[1]
            z1[i] = z[i] + key[2]
        ax.plot_surface(x1, y1, z1, color='green', alpha = .6)
    '''
    
    import plotly.express as px
    import pandas as pd
    df = pd.DataFrame(p, index= colors, columns=['x','y','z', 'Categories'])
    #df = px.data.iris()
    print(df)
    fig = px.scatter_3d(df, x='x', y='y', z='z', color=colors)
    #fig = px.scatter(df, x="sepal_width", y="sepal_length", color='petal_length')
    fig.update_traces(marker=dict(size=5))
    fig.show()
    print(p)

    

main()



import math
'''
n = 500
r = .5
n_0 = 0
a = (4*math.pi*(r*r))/n
d = math.sqrt(a)
m_0 = round(math.pi/d)
d_0 = math.pi/m_0
d_1 = a/d_0
x = []
y = []
z = []

for i in range(m_0-1):
    v = math.pi*(i+.5)/m_0
    m_1 = round(2*math.pi*math.sin(v)/d_1)
    for j in range(m_1-1):
        l = (2*math.pi*n)/m_1
        x.append(math.sin(v)*math.cos(l))
        y.append(math.sin(v) * math.sin(l))
        z.append(math.cos(v))
        n_0 += 1
print(n_0)
'''
import csv
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import random





