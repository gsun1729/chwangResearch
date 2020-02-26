"""
    Written by Christine Hwang, chwang14@jhu.edu
    Created on 20200206
    
    This code shows a 2D image on an interface.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QHBoxLayout,
                             QLabel, QSizePolicy, QSlider, QSpacerItem,
                             QVBoxLayout, QWidget)

from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg

from numba import jit, prange, njit
import numpy as np

from pathlib import Path
import sys

from time import time
import types
import cv2

colors =  {
            'lightest':"#eeeeee",
            'lighter':"#e5e5e5",
            'light':"#effffb",
            'himid':"#50d890",
            'midmid':"#1089ff",
            'lomid':"#4f98ca",
            'dark' :"#272727",
            'darker' :"#23374d",
}

numlabelsize = 22
txtlabelsize = 20

# STYLING
numfont = QtGui.QFont("Avenir Next") # requires macos
numfont.setPixelSize(numlabelsize)

txtfont = QtGui.QFont("Avenir Next") # requires macos
txtfont.setPixelSize(txtlabelsize)

brushes = { k: pg.mkBrush(c) for k, c in colors.items() }

pg.setConfigOptions(antialias=True)
pg.setConfigOption('background', colors['dark'])
pg.setConfigOption('foreground', colors['light'])

QPushButton_style = f"""
QPushButton{{
	color: {colors['light']};
	background-color: transparent;
	border: 1px solid #4589b2;
	padding: 5px;

}}

QPushButton::hover{{
	background-color: rgba(255,255,255,.2);
}}

QPushButton::pressed{{
	border: 1px solid {colors['himid']};
	background-color: rgba(0,0,0,.3);
}}"""

QLabel_style = f"""
QLabel{{
    color: {colors['light']};
}}
"""

QCheckBox_style = f"""
QCheckBox{{
    background-color: {colors['darker']};
    color: {colors['light']};
    padding:5px;
}}
"""
class filedialogdemo(QWidget):
    def __init__(self, parent=None):
        super(filedialogdemo, self).__init__(parent=parent)
        
        #setting up a QFileDialog
        self.one = QVBoxLayout(self)
        self.one.setAlignment(Qt.AlignTop)
        self.button = QtWidgets.QPushButton("Click to open a new tif image")
        self.button.clicked.connect(self.getfile)
        self.one.addWidget(self.button)
        self.setLayout(self.one)
        self.button.setStyleSheet(QPushButton_style)
        
        #showing a dog image using plot
        self.plot = pg.PlotWidget()      
        image = cv2.imread('C:\cygwin64\home\chrhw\Chaos\dog.tif')
        rotatedimage = np.transpose(image, (1, 0, 2))
        rotatedimage = np.flip(rotatedimage)
        rotatedimage = np.flip(rotatedimage, 0)
        imageadded = pg.ImageItem(rotatedimage)
        self.plot.addItem(imageadded)
        self.plot.hideAxis('left')
        self.plot.hideAxis('bottom')
        self.one.addWidget(self.plot)
        
    def getfile(self):
        #grabbing filename, user's wanted image
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open Image',
            'c:\\', "Image files (*.tif)")
        name = filename[0]
        
        #updating the image on interface to user's choice
        self.userimage = pg.PlotWidget()
        foundimage = cv2.imread(name)
        rotated = np.transpose(foundimage, (1, 0, 2))
        rotated = np.flip(rotated)
        rotated = np.flip(rotated, 0)
        imagetoadd = pg.ImageItem(rotated)
        self.plot.clear()
        self.plot.addItem(imagetoadd)

class Widget(QWidget):
    def __init__(self, app, parent=None):
        super(Widget, self).__init__(parent=parent)

        #setting up a graphics window
        self.setStyleSheet(f"Widget {{ background-color: {colors['dark']}; }}")
        self.setWindowTitle("Change the Picture!")
        
        #adding controls class to graphics window
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(filedialogdemo(parent=self))        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget(app)
    w.show()
    sys.exit(app.exec_())
