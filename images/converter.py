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


def jpg2ppm(inputfile, outputfolder, dataset="PENN"):
    """ 
    Convert files from JPG to PPM 
    
    Parameters:
    -----------
    inputfile: string
        path to a file containing paths and true labels
    outputfolder: string
        path to the folder where the PMM files are saved
    """
    fout = open(join(outputfolder, 'paths.txt'), 'w')
    pf = fh.ImagePaths(inputfile, "PENN", display=True)
    
    for line in pf:
        pathjpg, label = line
        root, pathimg = pf.extract_root()
        dirimg = dirname(pathimg)
        fname, ext = splitext(basename(pathimg))
        ppmpath = join(outputfolder, dirimg, fname+'.ppm')

        if not isdir(dirname(ppmpath)):
            os.makedirs(dirname(ppmpath))
        img = Image.open(pathjpg)
        img.save(ppmpath, "PPM")
        fout.write('%s %s\n' % (ppmpath, label))
    fout.close()
