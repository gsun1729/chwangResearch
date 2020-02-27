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
import os

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
currentimage = cv2.imread('C:\cygwin64\home\chrhw\Chaos\dog.tif')

class filedialog(QWidget):
    def __init__(self, parent=None):
        super(filedialog, self).__init__(parent=parent)
        
        #setting up a QFileDialog
        self.one = QVBoxLayout(self)
        self.one.setAlignment(Qt.AlignTop)
        self.button = QtWidgets.QPushButton("Click to open a new tif image")
        self.button2 = QtWidgets.QPushButton("Click to transform shown image and save")
        self.button3 = QtWidgets.QPushButton("Click to transform a whole directory")
        self.button.clicked.connect(self.getfile)
        self.button2.clicked.connect(self.transformfile)
        self.button3.clicked.connect(self.transformdir)
        self.one.addWidget(self.button)
        self.one.addWidget(self.button2)
        self.one.addWidget(self.button3)
        self.setLayout(self.one)
        self.button.setStyleSheet(QPushButton_style)
        self.button2.setStyleSheet(QPushButton_style)
        self.button3.setStyleSheet(QPushButton_style)
        
        #showing a dog image using plot
        self.plot = pg.PlotWidget()
        image = cv2.imread('C:\cygwin64\home\chrhw\Chaos\dog.tif')
        rotated = np.transpose(image, (1, 0, 2))
        rotated = np.flip(rotated)
        rotated = np.flip(rotated, 0)
        global currentimage
        currentimage = rotated
        imageadded = pg.ImageItem(rotated)
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
        image1 = cv2.imread(name)
        rotated1 = np.transpose(image1, (1, 0, 2))
        rotated1 = np.flip(rotated1)
        rotated1 = np.flip(rotated1, 0)
        global currentimage
        currentimage = rotated1
        imageadded1 = pg.ImageItem(rotated1)
        self.plot.clear()
        self.plot.addItem(imageadded1)
     
    def transformfile(self):
    
        #making change to user's image
        global currentimage
        rotated2 = np.flip(currentimage)
        currentimage = rotated2
        imageadded2 = pg.ImageItem(rotated2)
        self.plot.clear()
        self.plot.addItem(imageadded2)
        
        #saving changed image
        filename1 = QtGui.QFileDialog.getSaveFileName(self, "Save Image",
            'c:\\', "Tif Files (*.tif)")
        name1 = filename1[0]
        cv2.imwrite(name1, currentimage)
        
    def transformdir(self):
    
        #clearing plot image to show original dog
        image3 = cv2.imread('C:\cygwin64\home\chrhw\Chaos\dog.tif')
        rotated3 = np.transpose(image3, (1, 0, 2))
        rotated3 = np.flip(rotated3)
        rotated3 = np.flip(rotated3, 0)
        global currentimage
        currentimage = rotated3
        imageadded3 = pg.ImageItem(rotated3)
        self.plot.clear()
        self.plot.addItem(imageadded3)
        
        #grabbing directory from user choice
        dirname = QtGui.QFileDialog.getExistingDirectory(self, "Open Directory",
            'c:\\')
        
        #transforming all tif images in directory
        
        image_list = self.getFilenames(dirname)
        for i in image_list:
            newname = i[:-4] + '_transformed.tif'
            imagei = cv2.imread(i)
            rotatedi = np.transpose(imagei, (1, 0, 2))
            rotatedi = np.flip(rotatedi)
            rotatedi = np.flip(rotatedi, 0)
            rotatedi = np.flip(imagei)
            cv2.imwrite(newname, rotatedi)
        
    def getFilenames(self, root_directory, suffix = '.tif'):
        img_filelist = []
        for current_location, sub_directories, files in os.walk(root_directory):
            if files:
                for img_file in files:
                    if (suffix.lower() in img_file.lower()) and '_thumb_' not in img_file:
                        img_filelist.append(os.path.join(current_location, img_file))
        img_filelist.sort()

        return img_filelist
        
class Widget(QWidget):
    def __init__(self, app, parent=None):
        super(Widget, self).__init__(parent=parent)

        #setting up a graphics window
        self.setStyleSheet(f"Widget {{ background-color: {colors['dark']}; }}")
        self.setWindowTitle("Change the Picture!")
        
        #adding filedialog class to graphics window
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.addWidget(filedialog(parent=self))        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget(app)
    w.show()
    sys.exit(app.exec_())
