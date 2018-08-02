#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
This script creates a file containing the concatenation or the mean of feature
from two files.
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

def main(pathfeats1, pathfeats2, output=None, mean=False):
    pathfeats1 = fh.is_file(pathfeats1)
    pathfeats2 = fh.is_file(pathfeats2)
    if output:
        if fh.is_folder(output, boolean=True):
            fileout = join(output, 'concatenation.txt')
        else:
            fileout = fh.is_file(fileoutput)
    else:
        dirin = dirname(pathfeats1)
        fileout = join(dirin, 'concatenation.txt')
    fh.merge_features(pathfeats1, pathfeats2, fileout, mean=mean)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filefeats1', metavar='file_features_1', help='File containing paths to images, true labels and features')
    parser.add_argument('filefeats2', metavar='file_features_2', help='File containing paths to images, true labels and features')
    parser.add_argument('-o', '--output', help='File to save the file containing the concatenation or mean of the features', default=None)
    parser.add_argument('-m', '--mean', help='Generate the mean of the features instead of the concatenation', action="store_true")
    args = parser.parse_args()

    main(args.filefeats1, args.filefeats2, output=args.output, mean=args.mean)
