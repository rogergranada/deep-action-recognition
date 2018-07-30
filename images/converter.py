#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This script converts image files to other formats.
"""
import os
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import argparse
from PIL import Image
from os.path import isdir, join, dirname, basename, splitext

from classes import filehandler as fh


def img_converter(fileinput, fileoutput, to='ppm'):
    """ 
    Convert files from `of` to `to` types 

    Parameters:
    -----------
    fileinput: string
        path to the input image 
    fileoutput: string
        path to save the converted image
    to: string
        type of file to convert ('jpg'|'jpeg'|'ppm')
    """
    img = Image.open(fileinput)
    if img.format == 'JPEG' and to.lower() == 'ppm':
        img.save(fileoutput, 'PPM')
        return True
    elif img.format == 'PPM' and to.lower() in ['jpg', 'jpeg']:
        img.save(fileoutput, 'JPEG')
        return True
    return False


def convert_files(inputfile, outputfolder, dataset="PENN", to='ppm'):
    """ 
    Convert files from JPG|JPEG to PPM and vice-versa. 
    
    Parameters:
    -----------
    inputfile: string
        path to a file containing paths and true labels
    outputfolder: string
        path to the folder where the PPM files are saved
    dataset: string
        name of the dataset ('penn'|'dogcentric'|'ucf11'|'kscgr')
    to: string
        type of file to convert ('jpg'|'jpeg'|'ppm')
    """
    to = to.lower()
    fout = open(join(outputfolder, 'paths.txt'), 'w')
    pf = fh.ImagePaths(inputfile, dataset, display=True)
    
    for line in pf:
        pathinput, label = line
        root, pathimg = pf.extract_root()
        dirimg = dirname(pathimg)
        fname, ext = splitext(basename(pathimg))
        semipath = join(outputfolder, dirimg, fname)
        if not isdir(dirname(semipath)):
            os.makedirs(dirname(semipath))

        if to == 'ppm':
            fileoutput = semipath+'.ppm'
            converted = img_converter(pathinput, fileoutput, to=to)
        elif to == 'jpg':
            fileoutput = semipath+'.jpg'
            converted = img_converter(pathinput, fileoutput, to=to)
        if converted:
            fout.write('%s %s\n' % (fileoutput, label))
    fout.close()

