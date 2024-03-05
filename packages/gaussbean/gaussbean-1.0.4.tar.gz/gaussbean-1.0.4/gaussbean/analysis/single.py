#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Created on Sun Feb  18 02:38:00 2024

@author: leahghartman

Description : A file containing functions capable of analyzing a single image in a dataset.
"""
# import random needed packages that should already be installed
import sys

# make sure we can get modules from the other directory
sys.path.append('../utils/')

# import from other modules in the package
from gaussbean.utils import pre_utils, calc_utils

#########################
### START OF FUNCTIONS
#########################

def single_image_proj(xmargins, ymargins, imgpath='', imgar=[]):
    """ Runs a data analysis algorithm on a single image. Returns the FWHM in both transverse dimensions (across the image) as well as the cropped image for
    diagnostic, GIF, or movie purposes.

        Parameters
        ----------
        xmargins : integer
            A number (in pixels) of how far in the x-direction, on either side of the cropping point, the user wants the image to be cropped.
        ymargins : integer
            A number (in pixels) of how far in the y-direction, on either side of the cropping point, the user wants the image to be cropped.
        imgpath (OPTIONAL) : string
            The path to the image that the user wants to run through the median filter.
        imgar (OPTIONAL) : array
            Rather than a path to the image, one can also use the array of the image.
    """
    # set the array of the image to whatever the user specifies (either based on the image path OR an array that the user inputs)
    arrayimg = calc_utils.check_array(imgpath, imgar)

    # crop out as many dead pixels as possible (as long as the feature is SOMEWHAT in the middle of the image, this should be fine)
    initialcrop = pre_utils.crop_image(1212, 1012, 1000, 988, imgar=arrayimg)

    # find the centroid of the image with as many of the large dead pixels cropped out as possible
    centx, centy = calc_utils.find_centroid(imgar=initialcrop)

    # crop the image for the final time. This is the image that will be used in the rest of the analysis process
    finalimg = pre_utils.crop_image(centx, centy, xmargins, ymargins, imgar=initialcrop)

    # find the centroid AGAIN, but more accurately, so we can get a really nicely cropped image
    centx2, centy2 = calc_utils.find_centroid(imgar=finalimg)
    
    # use the projection along the y-axis to find the FWHM value for the beam along the y-axis
    yFWHM = calc_utils.find_FWHM(calc_utils.find_proj_y(imgar=finalimg))[0]
    
    # use the projection along the x-axis to find the FWHM value for the beam along the x-axis
    xFWHM = calc_utils.find_FWHM(calc_utils.find_proj_x(imgar=finalimg))[0]

    # return the FWHM value for the beam along the x- and y- directions, as well as the final cropped image, which can be used for diagnostic purposes
    return(xFWHM, yFWHM, finalimg)

########################################################

def single_image_line(xmargins, ymargins, xpixel=0, ypixel=0, toavg=0, imgpath='', imgar=[]):
    """ Returns the image path or the array of the image based on what the user has input into the function that's calling check_array(). This function shouldn't be
    called by the user at any point.

        Parameters
        ----------
        xmargins : integer
            A number (in pixels) of how far in the x-direction, on either side of the cropping point, the user wants the image to be cropped.
        ymargins : integer
            A number (in pixels) of how far in the y-direction, on either side of the cropping point, the user wants the image to be cropped.
        xpixel (OPTIONAL) : integer
            Specifies at which COLUMN the user wants to take the lineout along the image in pixels.
        ypixel (OPTIONAL) : integer
            Specifies at which ROW the user wants to take the lineout along the image in pixels.
        imgpath (OPTIONAL) : string
            The path to the image that the user wants to run through the median filter.
        imgar (OPTIONAL) : array
            Array of the image if the user wants to input an array into the function rather than just an image path.
    """
    # set the array of the image to whatever the user specifies (either based on the image path OR an array that the user inputs)
    arrayimg = calc_utils.check_array(imgpath, imgar)

    # crop out as many dead pixels as possible (as long as the feature is SOMEWHAT in the middle of the image, this should be fine)
    initialcrop = pre_utils.crop_image(1212, 1012, 1000, 988, imgar=arrayimg)

    # find the centroid of the image with as many of the large dead pixels cropped out as possible
    centx, centy = calc_utils.find_centroid(imgar=initialcrop)

    # crop the image for the final time. This is the image that will be used in the rest of the analysis process
    finalimg = pre_utils.crop_image(centx, centy, xmargins, ymargins, imgar=initialcrop)

    # find the centroid AGAIN, but more accurately, so we can get a really nicely cropped image
    centx2, centy2 = calc_utils.find_centroid(imgar=finalimg)

    # if statement to see if the user wants to use their own selected lineouts, or if they want to use the centroid
    if xpixel == 0 & ypixel == 0:
        xpixel = centx2
        ypixel = centy2
    
    # use the projection along the y-axis to find the FWHM value for the beam along the y-axis
    yFWHM = calc_utils.find_FWHM(calc_utils.find_line_y(xpixel, toavg=toavg, imgar=finalimg))[0]
    
    # use the projection along the x-axis to find the FWHM value for the beam along the x-axis
    xFWHM = calc_utils.find_FWHM(calc_utils.find_line_x(ypixel, toavg=toavg, imgar=finalimg))[0]

    # return the FWHM value for the beam along the x- and y- directions, as well as the final cropped image, which can be used for diagnostic purposes
    return(xFWHM, yFWHM, finalimg)
