#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
This module generates images with optical flow from a collection of images.
"""
import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import cv2
import numpy as np

from skimage import io
from os.path import realpath, splitext, basename, join, exists

from classes import filehandler as fh


def optical_flow(frame1, frame2, channels=False):
    """
    Generates the optical flow between two images.
    
    Parameters:
    -----------
    frame1 : string
        path to the first image
    frame2 : string
        path to the second image
    channels : boolean
        return separated channels (X and Y) of optical flow 
    """
    if not (exists(frame1) and exists(frame1)):
        logger.error('cannot find images: %s %s' % (frame1, frame2))
        sys.exit(0)
    img1 = cv2.imread(frame1)
    img2 = cv2.imread(frame2)
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    hsv = np.zeros_like(img1)
    hsv[...,1] = 255

    flow = cv2.calcOpticalFlowFarneback(gray1, gray2, flow=None, pyr_scale=0.5, 
                                        levels=3, winsize=10, iterations=5, 
                                        poly_n=5, poly_sigma=1.5, flags=0)
    if channels:
        return flow[...,0], flow[...,1]
    
    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return bgr

