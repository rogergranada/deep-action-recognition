#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
This module calculates the RGB mean of a collection of images.
"""
import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import cv2
import numpy as np
from os.path import realpath, splitext, basename, join, dirname

# customized files
from classes import progressbar
from classes import filehandler as fh


def mean_pixel(input, dirout):
    """
    Generate a pixelwise mean for a file containing paths to images.

    Parameters:
    -----------
    input : string
        File containing the path to all images and their true labels
    dirout : string
        Path to the output folder

    Notes:
    -------
    The function generates three files:
        fname.binaryproto : contains the pixelwise mean of the images
        fname.npy : numpy array containing the mean
        fname.png : image resulting of the mean
    """
    caffe = True
    try:
        from caffe.io import array_to_blobproto
    except:
        logger.warning('The system does not contain caffe.io to save as binaryproto')
        caffe = False
    from skimage import io

    input = realpath(input)
    fname = fh.filename(input, extension=False)
    dirout = fh.is_folder(dirout)
    fnameout = join(dirout, fname+'_mean')

    pf = fh.PathfileHandler(input)
    n = pf.nb_lines
    logger.info('Calculating mean for %d files.' % n)

    for nbline, arr in enumerate(pf):
        path = arr[0]
        img = io.imread(path)
        if nbline == 0:
            size = img.shape[1]
            mean = np.zeros((1, 3, size, size))
        mean[0][0] += img[:, :, 0]
        mean[0][1] += img[:, :, 1]
        mean[0][2] += img[:, :, 2]

    mean[0] /= n
    if caffe:
        blob = array_to_blobproto(mean)
        logger.info('Saving data into: %s' % fnameout+'.binaryproto')
        with open(fnameout+'.binaryproto', 'wb') as f:
            f.write(blob.SerializeToString())

    logger.info('Saving numpy matrix into: %s' % fnameout+'.npy')
    np.save(fnameout+'.npy', mean[0])
    mean_img = np.transpose(mean[0].astype(np.uint8), (1, 2, 0))
    logger.info('Saving mean image into: %s' % fnameout+'.png')
    io.imsave(fnameout+'.png', mean_img)
    

def mean_channel(input, mode='RGB'):
    """
    Calculate the mean of each channel from image files.

    Parameters:
    -----------
    input : string
        File containing the path to all images and their true labels
    mode : string
        Order of the channels in the output
    """
    mB, mG, mR = 0.0, 0.0, 0.0

    pf = fh.PathfileHandler(input)
    n = pf.nb_lines
    logger.info('Calculating mean for %d files.' % n)

    for path, label in pf:
        bgr_img = cv2.imread(path)
        b, g, r = cv2.split(bgr_img)
        mB += b.mean()
        mG += g.mean()
        mR += r.mean()
            
    mean_B = mB/n
    mean_G = mG/n
    mean_R = mR/n

    if mode == 'RGB':
        logger.info('Mean by channel: \nChannel R: %f\nChannel G: %f\nChannel B: %f' % (mean_R, mean_G, mean_B))
        return mean_R, mean_G, mean_B
    elif mode == 'BGR':
        logger.info('Mean by channel: \nChannel B: %f\nChannel G: %f\nChannel R: %f' % (mean_B, mean_G, mean_R))
        return mean_B, mean_G, mean_R
    else:
        logger.warning('Choose the correct mode (RGB or BGR). Returning RGB.')
        logger.info('Mean by channel: \nChannel R: %f\nChannel G: %f\nChannel B: %f' % (mean_R, mean_G, mean_B))
        return mean_R, mean_G, mean_B


def calculate_from_file(inputfile, by_pixel=True, channels='RGB', output=None):
    inputfile = fh.is_file(inputfile)
    if output:
        outfolder = fh.is_folder(output)
    else:
        outfolder = dirname(inputfile)
    fout = join(outfolder, 'mean')
    if by_pixel:
        mean_pixel(inputfile, outfolder)
    else:
        mean_channel(inputfile, mode=channels)
    
