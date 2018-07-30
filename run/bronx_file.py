#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
This script creates a file to use Bronx's optical flow. This file consisits of
path of the first image, the path of the second image, and the path of the output
optical flow image. In order to compute Bronx's optical flow, all images have to 
be in PPM format.

path_image_1 path_image_2 path_output
"""
import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import argparse
from os.path import join, dirname

# customized files
from classes import filehandler as fh
from misc import utils


def main(fileinput, dirout, output=None, window=2, dataset="PENN"):
    fileinput = fh.is_file(fileinput)
    dirout = fh.is_folder(dirout)
    if output:
        fileout = output
    else:
        dirin = dirname(fileinput)
        fileout = join(dirout, 'bronx_paths.txt')

    utils.bronx_file(fileinput, dirout, fileout, dataset, window=window)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('fileinput', metavar='file_input', help='File containing paths to JPG images to convert to PPM')
    parser.add_argument('outputfolder', metavar='output_folder', help='Path to the folder where the optical flow images are saved')
    parser.add_argument('-o', '--outputfile', help='File to save all paths', default=None)
    parser.add_argument('-w', '--window', help='Size of the window', default=2, type=int)
    parser.add_argument('-d', '--dataset', help='Name of the dataset', default="PENN")
    args = parser.parse_args()

    main(args.fileinput, args.outputfolder, output=args.outputfile, window=args.window, dataset=args.dataset)
