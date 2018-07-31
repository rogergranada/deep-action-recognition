#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
This script rewrites the paths of a file containing features with the paths
extracted from a ground truth file. Both files must have the same number of lines.
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

def main(fileground, filefeatures, output):
    fileground = fh.is_file(fileground)
    filefeatures = fh.is_file(filefeatures)
    if output:
        fileout = output
    else:
        fileout = join(dirname(filefeatures), 'tmp.txt')
    fh.change_paths(fileground, filefeatures, fileout)

    if not output:
        os.remove(filefeatures)
        os.rename(fileout, filefeatures)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('groundtruth', metavar='file_ground', help='File containing paths and true labels')
    parser.add_argument('featuresfile', metavar='file_feats', help='File containing paths and features')
    parser.add_argument('-o', '--output', help='File to save the output. In empty case, the output is the features file', default=None)
    args = parser.parse_args()

    main(args.groundtruth, args.featuresfile, args.output)
