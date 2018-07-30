#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
This script generates optical flow from two input images 
"""
import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import os
import argparse
from os.path import join, dirname, isdir

# customized files
from classes import filehandler as fh
from images import converter as cvr

def main(fileinput, output=None, dataset="PENN"):
    fileinput = fh.is_file(fileinput)
    if output:
        dirout = fh.is_folder(output)
    else:
        dirin = dirname(fileinput)
        dirout = join(dirin, 'JPG')
        if not isdir(dirout):
            os.makedirs(dirout)
    cvr.convert_files(inputfile, dirout, dataset, of='ppm', to='jpg')



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('fileinput', metavar='file_input', help='File containing paths to JPG images to convert to PPM')
    parser.add_argument('-o', '--output', help='Folder to store the new PPM files', default=None)
    parser.add_argument('-d', '--dataset', help='Name of the dataset', default="PENN")
    args = parser.parse_args()

    main(args.fileinput, output=args.output, dataset=args.dataset)
