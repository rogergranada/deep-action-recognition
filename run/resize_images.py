#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
This script resizes all images described in a file.
"""
import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import argparse

import os
from os.path import dirname, join, exists

# customized files
from images import imresize
from classes import filehandler

def main(inputfile, size, dataset, output=None):
    if output:
        dirout = filehandler.is_folder(output)
    else:
        dirout = join(dirname(inputfile), str(size))
        if not exists(dirout):
            os.makedirs(dirout)
    imresize.resize_pathfile(inputfile, dirout, dataset, size)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', metavar='file_input', 
                        help='path to the file containing images and true labels')    
    parser.add_argument('size', metavar='image_size', type=int, default=256,
                        help='new size to the images')
    parser.add_argument('dataset', metavar='dataset_name',
                        help='name of the dataset to be proceessed')
    parser.add_argument('-o', '--output', metavar='output_folder', default=None,
                        help='directory to save the output files')
    args = parser.parse_args()

    main(args.inputfile, args.size, args.dataset, output=args.output)
