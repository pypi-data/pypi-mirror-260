#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Created on Fri Jan  26 01:00:00 2024

@author: leahghartman

Description : A file for calculations/functions used in both single-image and full-dataset analysis.
"""
# import random needed packages that should already be installed
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.signal import peak_widths, find_peaks

#########################
### START OF FUNCTIONS
#########################

def check_array(imgpath, imgar):
    """ Returns the image path or the array of the image based on what the user has input into the function that's calling check_array(). This function shouldn't be
    called by the user at any point.

        Parameters
        ----------
        imgpath : string
            The path to the image that the user wants to run through the median filter.
        imgar : array
            Array of the image if the user wants to input an array into the function rather than just an image path.
    """
    # if the length of the image array is empty (the user didn't want to use an array), we use the image path instead
    if len(imgar) == 0:
        return(np.array(Image.open(imgpath).convert("L")))
    # if the length of the image array isn't zero, the user wants to use an array instead of the image path, so we return the array that was input
    else:
        return(imgar)

########################################################

def find_FWHM(imgdata):
    """ Returns the Full-Width at Half-Maximum of a set of data. This function uses the most prominent peak to find the FWHM.

        Parameters
        ----------
        imgdata : array
            Data corresponding to a singular axis or a set of data that the user wants to find the FWHM of using the most prominent peak in the data.
    """
    # find the most prominent peak
    peakmax = np.max(imgdata)

    # use the maximum value (coresponding to the most prominent peak) to find the peak of the curve to find the FWHM of
    peaks, _ = find_peaks(imgdata, prominence=(peakmax/1.1, peakmax*1.1))

    # find the width (FWHM) of the most prominent peak
    results_half = peak_widths(imgdata, peaks, rel_height=0.5)

    # return the FWHM calculation
    return(results_half[0])

########################################################

def find_centroid(imgpath='', imgar=[]):
    """ Returns x- and y-coordinate of the centroid based on the MAXIMUM INTENSITY of the image in each transverse dimension.

        Parameters
        ----------
        imgpath (OPTIONAL) : string
            The path to the image that the user wants to run through the median filter.
        imgar (OPTIONAL) : array
            Array of the image if the user wants to input an array into the function rather than just an image path.
    """
    # set the array of the image to whatever the user specifies (either based on the image path OR an array that the user inputs)
    arrayimg = check_array(imgpath, imgar)

    # find the x- and y-coordinates of the centroid by doing a projection of the entire image and finding the maximum value in the array for each dimension
    centx, centy = np.argmax(arrayimg.sum(axis=0)), np.argmax(arrayimg.sum(axis=1))

    # return the centroid's coordinates
    return(centx, centy)

########################################################

def find_proj_x(imgpath='', imgar=[]):
    """ Returns the projection of an image along the x-axis.

        Parameters
        ----------
        imgpath (OPTIONAL) : string
            The path to the image that the user wants to run through the median filter.
        imgar (OPTIONAL) : array
            Array of the image if the user wants to input an array into the function rather than just an image path.
    """
    # set the array of the image to whatever the user specifies (either based on the image path OR an array that the user inputs)
    arrayimg = check_array(imgpath, imgar)

    # return the summation of EACH column (so, this is the projection along the x-axis)
    return(arrayimg.sum(axis=0))

########################################################

def find_proj_y(imgpath='', imgar=[]):
    """ Returns the projection of an image along the y-axis.

        Parameters
        ----------
        imgpath (OPTIONAL) : string
            The path to the image that the user wants to run through the median filter.
        imgar (OPTIONAL) : array
            Array of the image if the user wants to input an array into the function rather than just an image path.
    """
    # set the array of the image to whatever the user specifies (either based on the image path OR an array that the user inputs)
    arrayimg = check_array(imgpath, imgar)
    
    # return the summation of EACH row (so, this is the projection along the y-axis)
    return(arrayimg.sum(axis=1))

########################################################

def find_line_x(ypixel, toavg=0, imgpath='', imgar=[]):
    """ Returns the lineout of an image along the x-axis and averages multiple columns of pixels if the user wants.

        Parameters
        ----------
        ypixel : integer
            Specifies at what ROW the user wants to take the lineout along the image in pixels. If you're going to find an x lineout, you need to specify a y-pixel
            along which the lineout is going to lie.
        toavg (OPTIONAL) : integer
            Specifies the number of pixels on EACH SIDE of the original pixel lineout the user wants to create a projection with (so, center lineout, plus 
            two lineouts on either side if "toavg" is set equal to 2).
        imgpath (OPTIONAL) : string
            The path to the image that the user wants to run through the median filter.
        imgar (OPTIONAL) : array
            Array of the image if the user wants to input an array into the function rather than just an image path.
    """
    # set the array of the image to whatever the user specifies (either based on the image path OR an array that the user inputs)
    arrayimg = check_array(imgpath, imgar)

    # this isn't really needed functionality, but added a while loop that appends the all the lineouts the user wants to a list
    lineoutar = []
    i = -toavg;
    while i <= toavg:
        lineoutar.append(np.array(arrayimg[ypixel+i, :]))
        i += 1;

    # return the total projection of all of the lineouts
    return(np.array(lineoutar).sum(axis=0))

########################################################

def find_line_y(xpixel, toavg=0, imgpath='', imgar=[]):
    """ Returns the lineout of an image along the y-axis and averages multiple rows of pixels if the user wants.

        Parameters
        ----------
        xpixel : integer
            Specifies at what COLUMN the user wants to take the lineout along the image in pixels. If you're going to find a y lineout, you need to specify an 
            x-pixel along which the lineout is going to lie.
        toavg (OPTIONAL) : integer
            Specifies the number of pixels on EACH SIDE of the original pixel lineout the user wants to average with (so, center lineout, plus two lineouts on
            either side if "toavg" is set equal to 2).
        imgpath (OPTIONAL) : string
            The path to the image that the user wants to run through the median filter.
        imgar (OPTIONAL) : array
            Array of the image if the user wants to input an array into the function rather than just an image path.
    """
    # set the array of the image to whatever the user specifies (either based on the image path OR an array that the user inputs)
    arrayimg = check_array(imgpath, imgar)

    # this isn't really needed functionality, but added a while loop that appends the all the lineouts the user wants to a list
    lineoutar = []
    i = -toavg;
    while i <= toavg:
        lineoutar.append(np.array(arrayimg[:, xpixel+i]))
        i += 1;

    # return the total projection of all of the lineouts
    return(np.array(lineoutar).sum(axis=0))