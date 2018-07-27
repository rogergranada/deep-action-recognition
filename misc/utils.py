#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This module contains scripts used by other functions
"""

import sys, os
sys.path.insert(0, '..')
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from os.path import realpath, splitext, basename, join, exists, isdir, dirname

from classes import filehandler as fh

def slide_window(dvideos, window):
    """
    Return pairs of images to generate the optical flow. These pairs contain 
    the first and the last image of the optical flow according to the size of the window.

    Parameters:
    -----------
    dvideos: dict
        Dictionary in the form:
        dic[label] = {'path_video_1': [frame_1, frame_2,...],
                      'path_video_2': [frame_1, frame_2,...],
                      ...
        }
    window: int
        size of the sliding window

    Returns:
    --------
    dout: dict
        Dictionary containing pairs of frames distant by `window`
    """
    dout = {}
    for label in sorted(dvideos):
        for path in sorted(dvideos[label]):
            vimgs = dvideos[label][path]
            pairs = []
            for n, img in enumerate(vimgs):
                next_img = n + window
                if len(vimgs) > next_img:
                    pairs.append((img, vimgs[next_img]))
                elif n+1 != len(vimgs):
                    pairs.append((img, vimgs[-1]))
            if dout.has_key(label):
                dout[label][path] = pairs
            else:
                dout[label] = {path: pairs}
    return dout


def bronx_file(inputfile, outputfolder, outputfile, dataset, window=2):
    """
    Create a file containing the path of the input images and the output
    image to geneate the Bronx's optical flow.
    
    Parameters:
    -----------
    inputfile: string
        path to the file containing the paths for all images
    outputfolder: string
        path to the folder where the optical flow will be saved
    outputfile: string
        path to save the output file
    window: int
        size of the window between frames in optical flow
    """
    logger.info('Creating file to generate Bronx optical flow from: %s' % inputfile)
    vid = fh.Videos(inputfile, dataset)
    dvideos = vid.label_videos()
    dpairs = slide_window(dvideos, window)

    fout = open(outputfile, 'w')
    for label in sorted(dpairs):
        for path in sorted(dpairs[label]):
            for img1, img2 in sorted(dpairs[label][path]):
                frame1 = join(path, img1+'.jpg')
                frame2 = join(path, img2+'.jpg')
                frameout = frame1.replace(vid.root, outputfolder)
                if not isdir(dirname(frameout)):
                    os.makedirs(dirname(frameout))
                fout.write('%s %s %s\n' % (frame1, frame2, frameout))

