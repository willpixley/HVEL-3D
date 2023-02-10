import plotly.express as px
import pandas as pd
import csv
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushBUtton, QLabel, 
    QLineEdit, QVBoxLayout, QGridLayout)
from PyQt6.QtCore import Qt
import sys
# pip install PyQt6

class Window(QWidget):
    def __init__(self):
        ## allows class to inherit elements from QWidget
        super().__init__()

app = QApplication(sys.argv) ## allows parameters to be passed from
# command line
window = Window()
window.show()
sys.exit(app.exec())
## base code