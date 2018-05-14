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
from os.path import join, dirname

# customized files
from classes import filehandler as fh
from images import opticalflow as of


def main(frame1, frame2, output=None, channels=False):
    image_1 = fh.is_file(frame1)
    image_2 = fh.is_file(frame2)
    if output:
        dirout = fh.is_folder(output)
    else:
        dirin = dirname(frame1)
        output = join(dirin, 'optical_flow.jpg')
    of.optical_flow(frame1, frame2, channels=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_1', metavar='file_1', help='First raw image to generate the optical flow')
    parser.add_argument('file_2', metavar='file_2', help='Second raw image to generate the optical flow')
    parser.add_argument('-o', '--output', help='Folder to store the optical flow image', default=None)
    parser.add_argument('-c', '--channels', action='store_true', help='Return separated X and Y channels')
    args = parser.parse_args()

    main(args.file_1, args.file_2, output=args.output, channels=args.channels)
