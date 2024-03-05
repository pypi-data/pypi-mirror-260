#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Created on Fri Jan  26 01:00:00 2024

@author: leahghartman

Description : A file for plotting utilities and functions that format plots.
"""
# import random needed packages that should already be installed
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from mpl_toolkits.axes_grid1 import make_axes_locatable

# import from other modules in the package
from gaussbean.utils import pre_utils, calc_utils

#########################
### START OF FUNCTIONS
#########################

def plot_beforeandafter(before, after, label='', clmap='plasma', fontsize=15):
    """ Returns a plot of an image before and after it has been run through a filter or altered in some way.

        Parameters
        ----------
        before : array
            The array associated with an image before it has been altered.
        after : array
            The array associated with an image after it has been altered.
        label (OPTIONAL) : string
            A string associated with WHAT is altering the image (could be "Median Filter" for example). Will be added to the title of the plot.
        clmap (OPTIONAL) : string
            The colormap that the user wants to use for the plots. This MUST be a colormap given by the matplotlib package.
        fontsize (OPTIONAL) : integer
            The fontsize used for the title of the plot. The axes labels are automatically formatted based on this number.
    """
    # format the figure so we have both images with before on the left and after on the right; add in some nice settings
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3))

    # set the title and axes labels for the image
    ax1.set_title('Image Before ' + label, fontsize=fontsize)
    ax2.set_title('Image After ' + label, fontsize=fontsize)
    ax1.set_ylabel('y pixels', fontsize=fontsize-3)
    ax1.set_xlabel('x pixels', fontsize=fontsize-3)
    
    ax2.set_ylabel('y pixels', fontsize=fontsize-3)
    ax2.set_xlabel('x pixels', fontsize=fontsize-3)

    # show the images
    ax1.imshow(before, cmap=clmap)
    ax2.imshow(after, cmap=clmap)

########################################################

def plot_median(mediansize, repeatamount=0, imgpath='', imgar=[], clmap='plasma', fontsize=15):
    """ Returns a plot of the image before and after it has been run through the median filter a specified number of times.

        Parameters
        ----------
        mediansize : integer
            The size of the median filter in pixels (generally want this to be small; from 2-10 pixels).
        repeatamount (OPTIONAL) : integer
            The times the user wants the filter to be run over the image.
        imgpath (OPTIONAL) : string
            The path to the image that the user wants to run through the median filter.
        imgar (OPTIONAL) : array
            Rather than a file path, if one wants to use an array to represent the image instead, it's possible.
        clmap (OPTIONAL) : string
            The colormap that the user wants to use for the plots. This MUST be a colormap given by the matplotlib package.
        fontsize (OPTIONAL) : integer
            The fontsize used for the title of the plot. The axes labels are automatically formatted based on this number.
    """
    # set the array of the image to whatever the user specifies (either based on the image path OR an array that the user inputs)
    arrayimg = calc_utils.check_array(imgpath, imgar)
    
    # get the image before the median filter is applied and after the filter is applied
    before = arrayimg
    after = pre_utils.thru_median(mediansize, repeatamount=repeatamount, imgar=arrayimg)

    # plot before and after
    plot_beforeandafter(before, after, label='Median Filter', clmap=clmap, fontsize=fontsize)

########################################################

def plot_lowpass(radius, imgpath='', imgar=[], clmap='plasma', fontsize=15):
    """ Returns a plot of the image before and after it has been run through a low-pass filter one time.

        Parameters
        ----------
        radius : integer
            The radius of the mask used for the low-pass filter in pixels.
        imgpath (OPTIONAL) : string
            The path to the image that the user wants to run through the median filter.
        imgar (OPTIONAL) : array
            Rather than a file path, if one wants to use an array to represent the image instead, it's possible.
        clmap (OPTIONAL) : string
            The colormap that the user wants to use for the plots. This MUST be a colormap given by the matplotlib package.
        fontsize (OPTIONAL) : integer
            The fontsize used for the title of the plot. The axes labels are automatically formatted based on this number.
    """
    # set the array of the image to whatever the user specifies (either based on the image path OR an array that the user inputs)
    arrayimg = calc_utils.check_array(imgpath, imgar)
    
    # get the image before the low-pass filter is applied and after the filter is applied
    before = arrayimg
    after = pre_utils.thru_lowpass(radius, imgar=arrayimg)

    # plot before and after
    plot_beforeandafter(before, after, label='Low-Pass Filter', clmap=clmap, fontsize=fontsize)

########################################################

def plot_medandlow(mediansize, radius, repeatamount=0, imgpath='', imgar=[], clmap='plasma', fontsize=15):
    """ Returns a plot of the original image, the image after ONLY a median filter has been applied, the image after ONLY a low-pass filter has been applied, and the image after BOTH a median filter and low-pass filter have been applied.

        Parameters
        ----------
        mediansize : integer
            The size of the median filter in pixels (generally want this to be small; from 2-10 pixels).
        radius : integer
            The radius of the mask used for the low-pass filter in pixels.
        repeatamount (OPTIONAL) : integer
            The times the user wants the MEDIAN filter to be run over the image.
        imgpath (OPTIONAL) : string
            The path to the image that the user wants to run through the median filter.
        imgar (OPTIONAL) : array
            Rather than an image path, one can opt to use an array of the image instead.
        clmap (OPTIONAL) : string
            The colormap that the user wants to use for the plots. This MUST be a colormap given by the matplotlib package.
        fontsize (OPTIONAL) : integer
            The fontsize used for the title of the plot. The axes labels are automatically formatted based on this number.
    """
    # set the array of the image to whatever the user specifies (either based on the image path OR an array that the user inputs)
    arrayimg = calc_utils.check_array(imgpath, imgar)
    
    # get the original image, the image after the median filter, the image after the low-pass filter, and the image after both filters
    original = arrayimg
    aftermed = pre_utils.thru_median(mediansize, repeatamount=repeatamount, imgar=arrayimg)
    afterlow = pre_utils.thru_lowpass(radius, imgar=arrayimg)
    afterboth = pre_utils.thru_lowpass(radius, imgar=aftermed)
    
    # create a figure with four subplots, show the images that are found above, and label each of them
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig.suptitle('Original Image Compared to Combinations of Filters', fontsize=fontsize, y=1.01)
    ax1.imshow(original, cmap=clmap)
    ax1.set_title('Original Image', fontsize=fontsize-3)
    ax2.imshow(aftermed, cmap=clmap)
    ax2.set_title('After Median Filter', fontsize=fontsize-3)
    ax3.imshow(afterlow, cmap=clmap)
    ax3.set_title('After Low-Pass Filter', fontsize=fontsize-3)
    ax4.imshow(afterboth, cmap=clmap)
    ax4.set_title('After Both Filters', fontsize=fontsize-3)

    # label all x- and y-axes
    fig.text(0.5, 0.04, 'x pixels', ha='center', fontsize=fontsize-3)
    fig.text(0.04, 0.5, 'y pixels', va='center', rotation='vertical', fontsize=fontsize-3)

    # fix the axes ticks so they only show for outer plots
    for ax in fig.get_axes():
        ax.label_outer()

########################################################

def plot_cropped(xpoint, ypoint, xmargins, ymargins, imgpath='', imgar=[], clmap='plasma', fontsize=15):
    """ Returns a plot of the image before and after it's been cropped.

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
    # get the array of the image before and after background subtraction
    before = calc_utils.check_array(imgpath, imgar)
    after = pre_utils.crop_image(xpoint, ypoint, xmargins, ymargins, imgar=before)
    
    # plot before and after doing background subtraction
    plot_beforeandafter(before=before, after=after, label='Cropping', clmap=clmap, fontsize=fontsize)

########################################################

def back_sub_plot(origpath='', backpath='', origimgar=[], backimgar=[], clmap='plasma', fontsize=15):
    """ Returns a plot of the image BEFORE and AFTER background subtraction.

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
        clmap (OPTIONAL) : string
            The colormap that the user wants to use for the plots. This MUST be a colormap given by the matplotlib package.
        fontsize (OPTIONAL) : integer
            The fontsize used for the title of the plot. The axes labels are automatically formatted based on this number.
    """
    # get the array of the image before and after background subtraction
    before = calc_utils.check_array(origpath, origimgar)
    backimg = calc_utils.check_array(backpath, backimgar)
    after = pre_utils.back_subtract(origimgar=before, backimgar=backimg)
    
    # plot before and after doing background subtraction
    plot_beforeandafter(before, after, label='Back-Sub', clmap=clmap, fontsize=fontsize)

########################################################

def plot_intensity_proj(imgpath='', imgar=[], clmap='plasma', fontsize=15):
    """ Returns a plot of the image with PROJECTIONS of the intensity on each axis.

        Parameters
        ----------
        imgpath (OPTIONAL) : string
            The path to the image that the user wants to run through the median filter.
        imgar (OPTIONAL) : array
            Rather than a path, if the user wants to use an array for the image instead, it's possible.
    """
    # set the array of the image to whatever the user specifies (either based on the image path OR an array that the user inputs)
    arrayimg = calc_utils.check_array(imgpath, imgar)

    # find the width and height of the image
    imheight, imwidth = np.shape(arrayimg)

    # create a numpy array so the axes will actually work on the right-hand-side graph (this isn't necessary on the top graph)
    positionsy = np.arange(1, imheight + 1, 1)
    positionsx = np.arange(1, imwidth + 1, 1)

    # customize the plots/plot as a whole (that is literally all that these lines of code do)
    fig, main_ax = plt.subplots(figsize=(7, 7))
    divider = make_axes_locatable(main_ax)
    top_ax = divider.append_axes("top", 1.05, pad=0.3, sharex=main_ax)
    right_ax = divider.append_axes("right", 1.05, pad=0.3, sharey=main_ax)

    # make the tick labels on the bottom sides of the top- and right-hand-side graphs disappear
    top_ax.xaxis.set_tick_params(labelbottom=False)
    right_ax.yaxis.set_tick_params(labelleft=False)
    right_ax.tick_params(labelrotation=-90)

    # give labels to all of the necessary axes and plots themselves (might have to play with the arangement of the right plot's title)
    main_ax.set_xlabel('x pixels', fontsize=fontsize)
    main_ax.set_ylabel('y pixels', fontsize=fontsize)
    top_ax.set_title('Intensity Profile (Projection) of Pixel Columns', fontsize=fontsize)
    right_ax.set_title('Intensity Profile (Projection) of Pixel Rows', x=1.13, y=-0.05, rotation=-90, fontsize=fontsize)

    # show the image as the main plot
    main_ax.imshow(arrayimg, cmap=clmap, extent=[0, imwidth, imheight, 0])

    # calculates the sum of the intensity values of all the pixels in every row and column
    cols = calc_utils.find_proj_x(imgar=arrayimg)
    rows = calc_utils.find_proj_y(imgar=arrayimg)

    # plots the right and top graphs with certain colors. If you want a different color, just change the 'color' input below
    v_prof, = right_ax.plot(rows, positionsy, color='black')
    h_prof, = top_ax.plot(cols, color='black')

    # show the entire figure
    plt.autoscale()
    plt.show()

########################################################

def plot_intensity_line(xpixel, ypixel, toavg=0, imgpath='', imgar=[], clmap='plasma', fontsize=15):
    """ Returns a plot of the image with LINEOUTS of the intensity on each axis. The location of the lineouts are specified by the user.

        Parameters
        ----------
        xpixel : integer
            Specifies the pixel at which the Y LINEOUT will be taken (for example, you want a y lineout, a straight line, you pick an x value, like x=0)
        ypixel : integer
            Specifies the pixel at which the X LINEOUT will be taken (for example, you want an x lineout, a straight line, you pick a y value, like y=0)
        toavg (OPTIONAL) : integer
            Specifies the number of pixels on EACH SIDE of the original pixel lineout the user wants to average with (so, center lineout, plus two lineouts on
            either side if "toavg" is set equal to 2).
        imgpath (OPTIONAL) : string
            The path to the image that the user wants to run through the median filter.
        imgar (OPTIONAL) : array
            Rather than a path, if the user wants to use an array for the image instead, it's possible.
    """
    # set the array of the image to whatever the user specifies (either based on the image path OR an array that the user inputs)
    arrayimg = calc_utils.check_array(imgpath, imgar)

    # find the width and height of the image
    imheight, imwidth = np.shape(arrayimg)

    # create a numpy array so the axes will actually work on the right-hand-side graph (this isn't necessary on the top graph)
    positionsy = np.arange(1, imheight + 1, 1)
    positionsx = np.arange(1, imwidth + 1, 1)

    # customize the plots/plot as a whole (that is literally all that these lines of code do)
    fig, main_ax = plt.subplots(figsize=(7, 7))
    divider = make_axes_locatable(main_ax)
    top_ax = divider.append_axes("top", 1.05, pad=0.3, sharex=main_ax)
    right_ax = divider.append_axes("right", 1.05, pad=0.3, sharey=main_ax)

    # make the tick labels on the bottom sides of the top- and right-hand-side graphs disappear
    top_ax.xaxis.set_tick_params(labelbottom=False)
    right_ax.yaxis.set_tick_params(labelleft=False)
    right_ax.tick_params(labelrotation=-90)

    # give labels to all of the necessary axes and plots themselves (might have to play with the arangement of the right plot's title)
    main_ax.set_xlabel('x pixels', fontsize=fontsize)
    main_ax.set_ylabel('y pixels', fontsize=fontsize)
    top_ax.set_title('Intensity Profile (Projection) of Pixel Columns', fontsize=fontsize)
    right_ax.set_title('Intensity Profile (Projection) of Pixel Rows', x=1.13, y=-0.05, rotation=-90, fontsize=fontsize)

    # show the image as the main plot
    main_ax.imshow(arrayimg, cmap=clmap, extent=[0, imwidth, imheight, 0])

    # calculates the sum of the intensity values of all the pixels in every row and column
    cols = calc_utils.find_line_x(ypixel, toavg=toavg, imgar=arrayimg)
    rows = calc_utils.find_line_y(xpixel, toavg=toavg, imgar=arrayimg)

    # plot the lineouts for nice visualization
    main_ax.plot(np.repeat(xpixel, len(arrayimg)), np.linspace(0, len(arrayimg), len(arrayimg)), color='y')
    main_ax.plot(np.linspace(0, len(arrayimg[0]), len(arrayimg[0])), np.repeat(ypixel, len(arrayimg[0])), color='y')
    main_ax.plot(xpixel, ypixel, '.', c='r')

    # plots the right and top graphs with certain colors. If you want a different color, just change the 'color' input below
    v_prof, = right_ax.plot(rows, positionsy, color='black')
    h_prof, = top_ax.plot(cols, color='black')

    # show the entire figure
    plt.autoscale()
    plt.show()
