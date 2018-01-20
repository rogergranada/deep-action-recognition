#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
This script extracts videos from a file containing paths to images.
"""
import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import argparse
from os.path import realpath, dirname, join

# customized files
from images import extract_videos

def main(fileinput, dataset, output=None):
    fileinput = realpath(fileinput)
    extract_videos.extract(fileinput, dataset, output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fileinput', metavar='file_input',
                        help='file containing paths and true labels')
    parser.add_argument('dataset', metavar='dataset_name',
                        help='name of the dataset to be proceessed')
    parser.add_argument('-o', '--output', metavar='output_folder', default=None,
                        help='directory to save the output files')
    args = parser.parse_args()
    main(args.fileinput, args.dataset, output=args.output)
