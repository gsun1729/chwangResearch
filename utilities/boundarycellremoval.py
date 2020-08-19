import tifffile as tf
import os
import cv2
import numpy as np


def getFilenames(root_directory, suffix = '.png'):
    img_filelist = []
    for current_location, sub_directories, files in os.walk(root_directory):
        if files:
            for img_file in files:
                if (suffix.lower() in img_file.lower()) and '_thumb_' not in img_file:
                    img_filelist.append(os.path.join(current_location, img_file))
    img_filelist.sort()

    return img_filelist

def removeBoundaries(image):
    '''
    This function takes an image and removes cells lying on the boundary of the image.
    Image has to be labeled (cells have unique ID numbers assigned).
    Returns modified image.

    Parameters
    ==========
    image : (np.ndarray)
        Image has to be grayscale, size not important.

    Returns
    ==========
    newimage : (np.ndarray)
        Image without boundary cells, also grayscale, same size as image.
    '''
    newimage = image
    rowmax = image.shape[0]
    colmax = image.shape[1]
    listtop = image[0, :]
    listbottom = image[rowmax - 1, :]
    listright = image[:, 0]
    listleft = image[:, colmax - 1]
    listall = listtop + listbottom + listright + listleft
    unique = np.unique(listall)
    for j in unique:
        newimage[image == j] = 0
    return newimage


img_filelist = getFilenames("C:\cygwin64\home\chrhw\Research\Practice")
for i in img_filelist:
    name = os.path.basename(i)
    newname = name[:-4] + '_removed.png'
    image = cv2.imread(i, 0)
    import matplotlib.pyplot as plt
    plt.imshow(removeBoundaries(image))
    plt.show()

def removeBoundaries(image):
    '''
    This function takes an image and removes cells lying on the boundary of the image.
    Image has to be labeled (cells have unique ID numbers assigned).
    Returns modified image.

    Parameters
    ==========
    image : (np.ndarray)
        Image has to be grayscale, size not important.

    Returns
    ==========
    newimage : (np.ndarray)
        Image without boundary cells, also grayscale, same size as image.
    '''
    newimage = image
    rowmax = image.shape[0]
    colmax = image.shape[1]
    listtop = image[0, :]
    listbottom = image[rowmax - 1, :]
    listright = image[:, 0]
    listleft = image[:, colmax - 1]
    listall = listtop + listbottom + listright + listleft
    unique = np.unique(listall)
    for j in unique:
        newimage[image == j] = 0
    return newimage
