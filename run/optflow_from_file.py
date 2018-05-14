#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
This script receives a file containing paths of images and generates the optical
flow to pairs of images according to the size of a window between images.
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
import cv2

def main(inputfile, output=None, window=1, channels=False):
    inputfile = fh.is_file(inputfile)
    if output:
        dirout = fh.is_folder(output)
    else:
        dirin = dirname(inputfile)

    # generate pairs of images to the optical flow
    dic = fh.imgpath2dic(inputfile)
    seqs = fh.pairs_of_paths(sorted(dic.keys()), window)

    # create optical flow for each pair
    for id1, id2 in seqs:
        flow = of.optical_flow(dic[id1], dic[id2], channels=channels)
        if channels:
            outflowX = join(dirin, str(id1)+'-'+str(id2)+'_x.jpg')
            outflowY = join(dirin, str(id1)+'-'+str(id2)+'_y.jpg')
            cv2.imwrite(outflowX, flow[0])
            cv2.imwrite(outflowY, flow[1])
        else:
            output = join(dirin, str(id1)+'-'+str(id2)+'.jpg')
            cv2.imwrite(output, flow)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', metavar='file_input', help='File containing paths to images')
    parser.add_argument('-o', '--output', help='Folder to store the optical flow image', default=None)
    parser.add_argument('-w', '--window', help='Size of the window to extract optical flow images', default=1, type=int)
    parser.add_argument('-c', '--channels', action='store_true', help='Return separated X and Y channels')
    args = parser.parse_args()

    main(args.inputfile, output=args.output, window=args.window, channels=args.channels)
