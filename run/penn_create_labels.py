#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
This script creates a file containing the paths and true labels for Penn Action dataset.

From the dataset downloaded from [1], create a new folder with resized images and path files
containing their respective paths and true labels.

[1] https://dreamdragon.github.io/PennAction/
"""
import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import argparse

import os
from os.path import dirname, join, exists

from datasets import pennaction
from classes import filehandler as fh

def main(inputfolder, imsize, output=None):
    """
    Parameters:
    -----------
    inputfolder : string
        path to the root folder containing the dataset
    imsize : int
        size of the new images
    output : string
        path to the folder where the new dataset will be saved
    """
    inputfolder = fh.is_folder(inputfolder)
    if output:
        dirout = fh.is_folder(output)
    else:
        dirout = join(inputfolder, str(imsize))
        if not exists(dirout):
            os.makedirs(dirout)
    # create a pathfile to the dataset
    pennaction.create_pathfile(inputfolder)
    # resize dataset to the new path
    #pennaction.resize_dataset(inputfolder, 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfolder', metavar='folder_input', 
                        help='path to the folder containing Penn dataset')    
    parser.add_argument('imsize', metavar='image_size', type=int, default=256,
                        help='new size to the images')
    parser.add_argument('-o', '--output', metavar='output_folder', default=None,
                        help='directory to save the output files')
    args = parser.parse_args()

    main(args.inputfolder, args.imsize, output=args.output)
