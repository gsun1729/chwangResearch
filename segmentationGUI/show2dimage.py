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
from PyQt5.QtGui import QPixmap, QImage, QColor, qRgb
import pyqtgraph as pg

from numba import jit, prange, njit
import numpy as np

from pathlib import Path
import sys
from PIL import Image
from time import time
import types
import os
from skimage import io
import scipy.io
from scipy.stats import iqr

import qimage2ndarray

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

class filedialog(QWidget):
    def __init__(self, parent=None):
        super(filedialog, self).__init__(parent=parent)
        
        #setting up a QFileDialog
        self.one = QVBoxLayout(self)
        self.one.setAlignment(Qt.AlignTop)
        #adding buttons for interactive choices
        self.button_getFile = QtWidgets.QPushButton("Click to open a new tif image")
        self.button_transformFile = QtWidgets.QPushButton("Click to transform shown image and save")
        self.button_transformDir = QtWidgets.QPushButton("Click to transform a whole directory")
        self.button_getFile.clicked.connect(self.getFile)
        self.button_transformFile.clicked.connect(self.transformFile)
        self.button_transformDir.clicked.connect(self.transformDir)
        self.one.addWidget(self.button_getFile)
        self.one.addWidget(self.button_transformFile)
        self.one.addWidget(self.button_transformDir)
        self.setLayout(self.one)
        self.button_getFile.setStyleSheet(QPushButton_style)
        self.button_transformFile.setStyleSheet(QPushButton_style)
        self.button_transformDir.setStyleSheet(QPushButton_style)
        self.slice_number = QLabel()
        self.slice_number.setStyleSheet(QLabel_style)
        self.one.addWidget(self.slice_number)
        
        #showing initial dog image
        #check file location when using this code on different computer!!
        dog_image = io.imread('dog.tif')
        rotated_dog = np.transpose(dog_image, (1, 0, 2))
        rotated_dog = np.flip(rotated_dog, 1)
        self.current_image = rotated_dog
        self.labels = QLabel(self)
        image_added = QPixmap('dog.tif')
        self.labels.setPixmap(image_added)
        self.one.addWidget(self.labels)

        
    def getFile(self):
        '''
        This function utilizes QFileDialog to open up a tif image of user's choice
        and displays it on the interface.
        Through QFileDialog, this function grabs the user's choice of file name
        and uses functions toQImage and other built-ins to display the associated image on the interface.
    
        Parameters
        ===========
        self: instance of class
        
        Outputs
        ===========
        Displays user's choice of tif file on interface
        No returns
        '''
        #grabbing file name of user's wanted image
        open_file = QtGui.QFileDialog.getOpenFileName(self, 'Open Image',
            'c:\\', "Image files (*.tif)")
        open_image = open_file[0]
        
        #updating self.current_image to user's choice
        self.user_image = io.imread(open_image)
        rotated_user = np.transpose(self.user_image, (1, 0, 2))
        rotated_user = np.flip(rotated_user, 1)
        self.current_image = rotated_user
        #grabbing slice info
        self.slices, self.rows, self.cols = self.user_image.shape
        self.start_index = self.slices//2
        #displaying a single slice at self.start_index
        self.slice_array = self.user_image[self.start_index, :, :]
        slice_image = self.toQImage()
        image_added1 = QPixmap.fromImage(slice_image)
        self.labels.setPixmap(image_added1)
        self.slice_number.setText("slice %s" % self.start_index)
     
    def transformFile(self):
        '''
        This function rotates the current image shown on the interface by 90 degrees 
        and utilizes QFileDialog to save the image under user's choice of file name.
        The transformed image is displayed on the interface.
    
        Parameters
        ===========
        self: instance of class
        
        Outputs
        ===========
        Writes to file the transformed image
        No returns
        '''
        #making change to user's image
        #change later (TRANSFORM)
        # TODO: Change np.flip into the appropriate transformation and test

        

        rotated_user1 = np.flip(self.current_image, 1)
        self.current_image = rotated_user1
        
        #saving changed image
        save_file = QtGui.QFileDialog.getSaveFileName(self, "Save Image",
            'c:\\', "Tif Files (*.tif)")
        save_image = save_file[0]
        io.imsave(save_image, self.current_image)
        
        #showing changed user's image
        rotated_user1 = np.transpose(rotated_user1, (1, 0, 2))
        rotated_user1 = np.flip(rotated_user1, 1)
        image_added2 = QPixmap(save_image)
        self.labels.setPixmap(image_added2)
        
    def transformDir(self):
        '''
        This function displays the original dog image,
        grabs user's choice of directory through QFileDialog,
        and transforms all tif images in that directory, writing them to file with the tag "_transformed.tif."
        Function getFileNames is used to get all file names in chosen directory.
        Here, transforming an image is rotating the image by 90 degrees.
    
        Parameters
        ===========
        self: instance of class
        
        Outputs
        ===========
        Writes to file all transformed images with the tag "_transformed.tif"
        No returns
        '''
        #showing original dog image
        dog_image = io.imread('dog.tif')
        rotated_dog = np.transpose(dog_image, (1, 0, 2))
        rotated_dog = np.flip(rotated_dog, 1)
        self.current_image = rotated_dog
        image_added3 = QPixmap('dog.tif')
        self.labels.setPixmap(image_added3)
        self.slice_number.clear()
        
        #grabbing directory from user choice
        dir_name = QtGui.QFileDialog.getExistingDirectory(self, "Open Directory",
            'c:\\')
        
        #transforming all tif images in directory
        image_list = self.getFileNames(dir_name)
        for i in image_list:
            new_name = i[:-4] + '_transformed.tif'
            image_i = io.imread(i)
            rotated_i = np.transpose(image_i, (1, 0, 2))
            rotated_i = np.flip(rotated_i, 1)
            new_i = np.flip(rotated_i, 1)
            io.imsave(new_name, new_i)
        
    def getFileNames(self, root_directory, suffix = '.tif'):
        '''
        This function grabs all tif file names in a given directory
        and makes and returns a list of the names.
    
        Parameters
        ===========
        self: instance of class
        root_directory: directory of choice
        suffix = '.tif': suffix of file names wanted is '.tif'
        
        Outputs
        ===========
        Returns img_filelist: list of file names with suffix = '.tif' in given directory
        '''
        img_filelist = []
        for current_location, sub_directories, files in os.walk(root_directory):
            if files:
                for img_file in files:
                    if (suffix.lower() in img_file.lower()) and '_thumb_' not in img_file:
                        img_filelist.append(os.path.join(current_location, img_file))
        img_filelist.sort()

        return img_filelist
    
    def wheelEvent(self, event):
        '''
        This function redirects wheelEvent so when wheel is rotated up, function updateSlice is called to increase the slice viewed, and
        when wheel is rotated down, function updateSlice is called to decrease the slice viewed.
    
        Parameters
        ===========
        self: instance of class
        event: wheel event
        
        Outputs
        ===========
        Calls function updateSlice with appropriate slice number
        No returns
        '''
        if (event.angleDelta().y() > 0):
            self.start_index = (self.start_index + 1) % self.slices
        elif (event.angleDelta().y() < 0):
            self.start_index = (self.start_index - 1) % self.slices
        self.updateSlice()
    
    def updateSlice(self):
        '''
        This function updates the slice viewed on the interface depending on the index provided by self.
        
        Parameters
        ===========
        self: instance of class
        
        Outputs
        ===========
        Displays appropriate slice on the interface
        No returns
        '''
        self.slice_array = self.user_image[self.start_index, :, :]
        new_slice = self.toQImage()
        image_added4 = QPixmap.fromImage(new_slice)
        self.labels.setPixmap(image_added4)
        self.slice_number.setText("slice %s" % self.start_index)
    
    def toQImage(self):
        '''
        This function utilizes qimage2ndarray to transform a slice array to a QImage.
    
        Parameters
        ===========
        self: instance of class
        
        Outputs
        ===========
        Returns slice_QImage: QImage made from slice array at self.slice_array
        '''
        slice_QImage = qimage2ndarray.array2qimage(self.slice_array)
        return slice_QImage
    
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
