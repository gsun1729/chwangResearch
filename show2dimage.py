"""
    Written by Christine Hwang, chwang14@jhu.edu
    Created on 20200206
    
    This code allows the viewing of tif images on an interface
    and provides the user with the following three interactive choices.
    
    1. Open up a different tif image.
    2. Transform the tif image seen and save the transformed image.
    3. Transform a whole directory of tif images and save the transformed images.
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

#styling
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
currentImage = cv2.imread('C:\cygwin64\home\chrhw\Research\dog.tif')

class filedialog(QWidget):
    def __init__(self, parent=None):
        super(filedialog, self).__init__(parent=parent)
        
        #setting up a QFileDialog
        self.one = QVBoxLayout(self)
        self.one.setAlignment(Qt.AlignTop)
        self.buttonOpen = QtWidgets.QPushButton("Click to open a new tif image")
        self.buttonTransform = QtWidgets.QPushButton("Click to transform shown image and save")
        self.buttonDirTransform = QtWidgets.QPushButton("Click to transform a whole directory")
        self.buttonOpen.clicked.connect(self.getFile)
        self.buttonTransform.clicked.connect(self.transformFile)
        self.buttonDirTransform.clicked.connect(self.transformDir)
        self.one.addWidget(self.buttonOpen)
        self.one.addWidget(self.buttonTransform)
        self.one.addWidget(self.buttonDirTransform)
        self.setLayout(self.one)
        self.buttonOpen.setStyleSheet(QPushButton_style)
        self.buttonTransform.setStyleSheet(QPushButton_style)
        self.buttonDirTransform.setStyleSheet(QPushButton_style)
        
        #showing a dog image using plot
        #check file location when using this code on different computer!!
        self.plot = pg.PlotWidget()
        dogImage = cv2.imread('C:\cygwin64\home\chrhw\Research\dog.tif')
        rotatedDog = np.transpose(dogImage, (1, 0, 2))
        rotatedDog = np.flip(rotatedDog)
        rotatedDog = np.flip(rotatedDog, 0)
        global currentImage
        currentImage = rotatedDog
        imageAdded = pg.ImageItem(rotatedDog)
        self.plot.addItem(imageAdded)
        self.plot.hideAxis('left')
        self.plot.hideAxis('bottom')
        self.one.addWidget(self.plot)
        
    def getFile(self):
    
        #grabbing file name of user's wanted image
        openFile = QtGui.QFileDialog.getOpenFileName(self, 'Open Image',
            'c:\\', "Image files (*.tif)")
        openImage = openFile[0]
        
        #updating the image on interface to user's choice
        self.userImage = pg.PlotWidget()
        userImage = cv2.imread(openImage)
        rotatedUser = np.transpose(userImage, (1, 0, 2))
        rotatedUser = np.flip(rotatedUser)
        rotatedUser = np.flip(rotatedUser, 0)
        global currentImage
        currentImage = rotatedUser
        imageAdded1 = pg.ImageItem(rotatedUser)
        self.plot.clear()
        self.plot.addItem(imageAdded1)
     
    def transformFile(self):
    
        #making change to user's image
        #change later
        global currentImage
        rotatedUser1 = np.flip(currentImage)
        currentImage = rotatedUser1
        
        #showing changed user's image
        rotatedUser1 = np.transpose(rotatedUser1, (1, 0, 2))
        rotatedUser1 = np.flip(rotatedUser1)
        rotatedUser1 = np.flip(rotatedUser1, 0)
        imageAdded2 = pg.ImageItem(rotatedUser1)
        self.plot.clear()
        self.plot.addItem(imageAdded2)
        
        #saving changed image
        saveFile = QtGui.QFileDialog.getSaveFileName(self, "Save Image",
            'c:\\', "Tif Files (*.tif)")
        saveImage = saveFile[0]
        cv2.imwrite(saveImage, currentImage)
        
    def transformDir(self):
    
        #clearing plot image to show original dog
        dogImage = cv2.imread('C:\cygwin64\home\chrhw\Research\dog.tif')
        rotatedDog = np.transpose(dogImage, (1, 0, 2))
        rotatedDog = np.flip(rotatedDog)
        rotatedDog = np.flip(rotatedDog, 0)
        global currentImage
        currentImage = rotatedDog
        imageAdded3 = pg.ImageItem(rotatedDog)
        self.plot.clear()
        self.plot.addItem(imageAdded3)
        
        #grabbing directory from user choice
        dirName = QtGui.QFileDialog.getExistingDirectory(self, "Open Directory",
            'c:\\')
        
        #transforming all tif images in directory
        
        image_list = self.getFileNames(dirName)
        for i in image_list:
            newName = i[:-4] + '_transformed.tif'
            imagei = cv2.imread(i)
            rotatedi = np.transpose(imagei, (1, 0, 2))
            rotatedi = np.flip(rotatedi)
            rotatedi = np.flip(rotatedi, 0)
            newi = np.flip(rotatedi)
            cv2.imwrite(newName, newi)
        
    def getFileNames(self, root_directory, suffix = '.tif'):
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
