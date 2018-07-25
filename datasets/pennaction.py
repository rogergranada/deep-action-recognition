#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
This script deals with Penn Action [1] dataset.

[1] https://dreamdragon.github.io/PennAction/
"""
import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import os
from os.path import join, dirname

def create_pathfile(inputfolder):
    """
    Create `path.txt` file containing the paths 
    and true labels of all images in the dataset

    Parameters:
    -----------
    inputfolder: string
        path to the root folder of the dataset
    """
    imgdir = join(inputfolder, 'frames')
    lbldir = join(inputfolder, 'labels')

    for root, dirs, files in sorted(os.walk(imgdir, topdown=False)):
        print root, dirs, files 
        for name in files:
            print(os.path.join(root, name))
            break
        break



