#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
This script will take all the images from inputfile and classify according the neural net.
It will create an output file that have the path from the image, the correct label, and the predict label.
"""
import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import os
import argparse
from os.path import dirname, join, exists

# customized files
from classes import filehandler
from images import rgbmean


def main(inputfile, by_pixel=False, channels='RGB', output=None):
    inputfile = filehandler.is_file(inputfile)
    if output:
        dirout = filehandler.is_folder(output)
    else:
        dirin = dirname(inputfile)
        dirout = join(dirin, 'mean')
        if not exists(dirout):
            os.makedirs(dirout)
    rgbmean.calculate_from_file(inputfile, by_pixel=by_pixel, channels=channels, output=dirout)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', metavar='file_input', help='File containing paths to images and true labels')
    parser.add_argument('-o', '--output', help='Folder to record files with the mean', default=None)
    parser.add_argument('-c', '--channels', help='Order of the channels', default='RGB')
    parser.add_argument('-p', '--pixel', action='store_true', help='get the mean by pixel')
    args = parser.parse_args()

    main(args.inputfile, by_pixel=args.pixel, channels=args.channels, output=args.output)
