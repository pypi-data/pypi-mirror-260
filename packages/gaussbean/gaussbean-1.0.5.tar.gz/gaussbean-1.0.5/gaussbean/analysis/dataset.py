#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Created on Sun Feb  18 02:37:00 2024

@author: leahghartman

Description : A file containing functions capable of analyzing a full dataset of images.
"""
# import random needed packages that should already be installed
import numpy as np
from PIL import Image

# import from other modules in the package
from gaussbean.analysis import single

#########################
### START OF FUNCTIONS
#########################

def full_set_proj(imglist, xmargins, ymargins):
    """ Returns a list of FWHM values (in microns) for both x- and y-axes as well as all cropped images used for analysis. This function is based on projections of 
    each of the images.

        Parameters
        ----------
        imglist : array
            Array of images (this needs to be a set of SORTED image paths (so, 1.tiff, 2.tiff, etc.).
        xmargins : integer
            How many pixels on each side of the beam (in the x-direction, relative to the centroid of the image) to be used as a buffer for cropping.
        ymargins : integer
            How many pixels on each side of the beam (in the y-direction, relative to the centroid of the image) to be used as a buffer for cropping.
    """
    # create empty lists for FWHM in x- and y-directions as well as an empty list for all of the cropped images
    xlist = []
    ylist = []
    croppedimgs = []

    # for loop that cycles through all of the images and finds the FWHM along each axis (using PROJECTIONS)
    for i in imglist:
        # find the FWHM in both transverse dimensions as well as the cropped images used for processing
        xFWHM, yFWHM, croppedimg = single.single_image_proj(xmargins, ymargins, imgar=np.array(Image.open(i)))

        # append everything to their respective empty lists
        croppedimgs.append(croppedimg)
        xlist.append(xFWHM)
        ylist.append(yFWHM)

    # return everything we want
    return(xlist, ylist, croppedimgs)


def full_set_line(imglist, xmargins, ymargins, xpixel=0, ypixel=0):
    """ Returns a list of FWHM values in the x- and y-directions as well as a list of all cropped images used for analysis. This function is based on lineouts 
    either provided by the user or the centroid of the image is used.

        Parameters
        __________
        imglist : array
            Array of image paths (this needs to be a set of SORTED image paths (so, 1.tiff, 2.tiff, etc.).
        xmargins : integer
            How many pixels on each side of the beam (in the x-direction, relative to the centroid of the image) to be used as a buffer for cropping.
        ymargins : integer
            How many pixels on each side of the bean (in the y-direction, relative to the centroid of the image) to be used as a buffer for cropping.
        xpixel (OPTIONAL) : integer
            The column of pixels at which a y-lineout will be taken.
        ypixel (OPTIONAL) : integer
            The row of pixels at which an x-lineout will be taken.
    """
    # create empty lists for FWHM in x- and y-directions as well as an empty list for all of the cropped images
    xlist = []
    ylist = []
    croppedimgs = []

    # just run the code in a for loop like normal; if x- and y- pixels are not specified, the code will just automatically use the centroid instead
    for i in imglist:
        # find the FWHM in both transverse dimensions as well as the cropped images used for processing
        xFWHM, yFWHM, croppedimg = single.sing_image_line(xmargins, ymargins, xpixel=xpixel, ypixel=ypixel, imgar=np.array(Image.open(i)))

        # append everything to their respective lists
        croppedimgs.append(croppedimg)
        xlist.append(xFWHM)
        ylist.append(yFWHM)

    # return everything we want
    return(xlist, ylist, croppedimgs)
