#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
This script resizes images
"""
import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import os
import cv2
from os.path import realpath, join, exists, dirname

# customized files
from classes import filehandler, progressbar

def resize_image(img, size):
    """
    Resize a image to `size`

    Parameters:
    -----------
    img : numpy.ndarray
        image after read by cv2.imread()
    size : int
        new size of the image
    """
    width = int(img.shape[1])
    height = int(img.shape[0])
    new_width = 0
    crop = 0

    if width < height:
        new_width = size
        new_height = (size * height) / width
        crop = new_height - size
        img = cv2.resize(img, (new_width, new_height), 0, 0, cv2.INTER_CUBIC)
        img = img[crop / 2:size + (crop / 2), :]
    else:
        new_height = size
        new_width = (size * width) / height
        crop = new_width - size      
        img = cv2.resize(img, (new_width, new_height), 0, 0, cv2.INTER_CUBIC)
        img = img[:, crop / 2:size + (crop / 2)]
    return img


def resize_file(imgpath, outpath, size):
    """
    Receives the path of an image and resize it to `size`
    
    Parameters:
    -----------
    impath : string
        path to the input image
    outpath : string
        path to the output image
    size : int
        new size of the image
    """
    imgpath = realpath(imgpath)
    outpath = realpath(outpath)
    img = cv2.imread(imgpath)
    img = resize_image(img, size)
    cv2.imwrite(outpath, img)
    return img


def resize_pathfile(inputfile, outputfolder, dataset, size):
    """
    Receives the path of a file and resize all images in this
    file to size=`size`
    
    Parameters:
    -----------
    input : string
        path to the input file containing multiple images
    output : string
        path to the output folder
    size : int
        new size of the image
    """
    inputfile = filehandler.is_file(inputfile)
    outputfolder = filehandler.is_folder(outputfolder)
    fname = filehandler.add_text2path(inputfile, size, withfolder=False)
    fout = open(join(outputfolder, fname), 'w')

    logger.info('resizing images to: %dx%d' % (size, size))
    logger.info('saving output file at: %s' % join(outputfolder, fname))

    pf = filehandler.ImagePaths(inputfile, dataset)
    for impath, label in pf:
        #logger.info('processing file: %s' % impath)
        _, fimg = pf.extract_root()
        outpath = join(outputfolder, fimg)

        #logger.info('saving file: %s' % fimg)
        imfolder = dirname(outpath)
        if not exists(imfolder):
            os.makedirs(imfolder)
        
        resize_file(impath, outpath, size)
        fout.write('%s %s\n' % (outpath, str(label)))

