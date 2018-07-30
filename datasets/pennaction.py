#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
This script deals with Penn Action [1] dataset.

[1] https://dreamdragon.github.io/PennAction/
"""
import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from scipy.io import loadmat

import os
from os.path import join, dirname, basename

from classes import filehandler as fh
from classes import fileconfig as fc
from images import imresize

def create_pathfile(inputfolder):
    """
    Create 3 files: `path.txt`, `train.txt` and `test.txt` 
    `path.txt` file contains the paths and true label of all images in the dataset
    `train.txt` and `test.txt` contain paths and true labels separatedly.

    Parameters:
    -----------
    inputfolder: string
        path to the root folder of the dataset
    """
    #load configuration of the dataset
    conf = fc.Configuration()
    dlabels = conf.id_label("PENN")

    imgdir = join(inputfolder, 'frames')
    lbldir = join(inputfolder, 'labels')
    paths = join(inputfolder, 'paths.txt')
    train = join(inputfolder, 'train.txt')
    test = join(inputfolder, 'test.txt')

    with open(paths, 'w') as fpaths, \
         open(train, 'w') as ftrain, \
         open(test,  'w') as ftest: 

        for root, dirs, files in sorted(os.walk(imgdir, topdown=False)):
            current = basename(root)
            if current and current != 'frames':
                labels = join(lbldir, current+'.mat')
                labels = fh.is_file(labels)
                mat = loadmat(labels)
                train = mat['train'][0][0]
                action = mat['action'][0]
                idact = dlabels[action]
                for fname in sorted(files):
                    path = join(root, fname)
                    if train == 1:
                        ftrain.write('%s %d\n' % (path, idact))
                    else:
                        ftest.write('%s %d\n' % (path, idact))
                    fpaths.write('%s %d\n' % (path, idact))


