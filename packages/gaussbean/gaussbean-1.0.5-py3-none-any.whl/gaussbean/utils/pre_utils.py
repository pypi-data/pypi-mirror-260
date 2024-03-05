#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Created on Fri Jan  26 01:00:00 2024

@author: leahghartman

Description : A file for functions that make images look prettier.
"""
# import random needed packages that should already be installed
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy import ndimage

# import from other modules in the package
from gaussbean.utils import calc_utils

#########################
### START OF FUNCTIONS
#########################

def thru_median(mediansize, repeatamount=0, imgpath='', imgar=[]):
    """ Returns an image in the form of an array that has been run through a median filter a specified number of times.
    
        Parameters
        ----------
        mediansize : integer
            The size of the median filter in pixels (generally want this to be small; from 2-10 pixels).
        repeatamount (OPTIONAL) : integer
            The number of times the user wants to run the image through the median filter. Default is to run over the image only once.
        imgpath (OPTIONAL) : string
            The path to the image that the user wants to run through the median filter.
        imgar (OPTIONAL) : array
            Array of the image if the user wants to input an array into the function rather than just an image path.
    """
    # set the array of the image to whatever the user specifies (either based on the image path OR an array that the user inputs)
    arrayimg = calc_utils.check_array(imgpath, imgar)

    # create an array for the median filter images and append to this array when a change to the image is made
    result = [ndimage.median_filter(np.array(arrayimg), size=mediansize)]

    # for loop to repeat the number of times the median filter is run over the image
    for i in range(2, repeatamount+1):
        result.append(ndimage.median_filter(result[i-2], size=mediansize))

    # return the result after running through the median filter
    return(result[-1])

########################################################

def thru_lowpass(radius, imgpath='', imgar=[]):
    """ Returns an image in the form of an array that has been run through a low-pass filter one time.

        Parameters
        ----------
        radius : integer
            The radius of the mask used for the low-pass filter in pixels.
        imgpath (OPTIONAL) : string
            The path to the image that the user wants to run through the median filter.
        arimg (OPTIONAL) : array
            Array of the image if the user wants to input an array into the function rather than just an image path.
    """
    # set the array of the image to whatever the user specifies (either based on the image path OR an array that the user inputs)
    arrayimg = calc_utils.check_array(imgpath, imgar)
    
    # perform the fourier transform and save the complex output
    ft = np.fft.fft2(arrayimg, axes=(0,1))

    # shift the origin to the center of the image
    ft_shift = np.fft.fftshift(ft)

    # create circular mask using size specified in the cell above
    mask = np.zeros_like(arrayimg) # --> returns an array of zeros the same shape as the image
    cy = mask.shape[0] // 2
    cx = mask.shape[1] // 2
    cv2.circle(mask, (cx,cy), radius, (255,255,255), -1)[0]

    # blur the mask to prevent artifacts on the image
    finalmask = cv2.GaussianBlur(mask, (19,19), 0)

    # apply the mask to the shifted fourier transform of the image
    masked_ft_shifted = np.multiply(ft_shift,finalmask) / 255

    # shift origin from center to upper left corner (basically return the image to its original state before using fft to get back)
    back_ishift_masked = np.fft.ifftshift(masked_ft_shifted)

    # do inverse fft and save as complex output
    filteredimg = np.fft.ifft2(back_ishift_masked, axes=(0,1))

    # combine complex real and imaginary components to form (the magnitude for) the original image again
    filteredimg = np.abs(filteredimg).clip(0,255).astype(np.uint8)

    # return the filtered image
    return(filteredimg)

########################################################

def back_subtract(origpath='', backpath='', origimgar=[], backimgar=[]):
    """ Returns an image in the form of an array after the background image provided is subtracted from the original image.

        Parameters
        ----------
        origpath (OPTIONAL) : string
            The path of the original image to be used (the image before background subtraction).
        backpath (OPTIONAL) : string
            The path of the background image to be subtracted from the original image (this should be a blank image).
        origimgar (OPTIONAL) : array
            Rather than an image path, one can opt to use an array instead. This is the array of the original image to be used (before background subtraction).
        backimgar (OPTIONAL) : array
            Rather than an image path, one can opt to use an array instead. This is the array of the background image to be used (a blank image).
    """
    # set the array of the original image to whatever the user specifies (either based on the image path OR an array that the user inputs)
    origimg = calc_utils.check_array(origpath, origimgar)
    
    # set the array of the original image to whatever the user specifies (either based on the image path OR an array that the user inputs)
    backimg = calc_utils.check_array(backpath, backimgar)

    # return the array of the image after background subtraction
    return(origimg - backimg)

########################################################

def crop_image(xpoint, ypoint, xmargins, ymargins, imgpath='', imgar=[]):
    """ Returns an image in the form of an array after being cropped the amount specified around the point specified.

        Parameters
        ----------
        xpoint : integer
            x-coordinate of the point at which the crop will be occurring.
        ypoint : integer
            y-coordinate of the point at which the crop will be occurring.
        xmargins : integer
            A number (in pixels) of how far in the x-direction, on either side of the cropping point, the user wants the image to be cropped.
        ymargins : integer
            A number (in pixels) of how far in the y-direction, on either side of the cropping point, the user wants the image to be cropped.
        imgpath (OPTIONAL) : string
            The path to the image that the user wants to run through the median filter.
        imgar (OPTIONAL) : array
            Array of the image if the user wants to input an array into the function rather than just an image path.
    """
    # set the array of the original image to whatever the user specifies (either based on the image path OR an array that the user inputs)
    arrayimg = calc_utils.check_array(imgpath, imgar)

    # crop the image
    finalimgar = arrayimg[round(ypoint-ymargins):round(ypoint+ymargins), round(xpoint-xmargins):round(xpoint+xmargins)]

    # return the cropped image array
    return(finalimgar)
