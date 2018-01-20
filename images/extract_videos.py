#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import argparse
from os.path import realpath, dirname, join, isfile, isdir

# customized files
from classes import filehandler

def extract(inputfile, dataset, output=None):
    """
    Extract frames corresponding to videos in ``inputfile``
    
    Parameters
    ----------
    inputfile : string
        file containing paths and true labels
    datasets : string (dogs|kitchen|ucf11)
        name of the dataset
    output : string
        folder to save output files 

    Output
    -------
        save files containing the name of the action (from the path) and its
        respective frames. Create also a file named ``videos.txt`` containing
        a list of all generated files.
    """
    inputfile = filehandler.is_file(inputfile)
    if output:
        dirout = filehandler.is_folder(output)
    else:
        dirout = dirname(inputfile)

    fh = filehandler.Videos(inputfile, dataset)
    dvideos = fh.extract_videos()
    fvideos = open(join(dirout, 'videos.txt'), 'w')
    for video in dvideos:
        fname = video+'.txt'
        vname = join(dirout, fname)
        fvideos.write('%s\n' % vname)
        with open(vname, 'w') as fout:
            for path, y in sorted(dvideos[video]):
                fout.write('%s %s\n' % (path, y))
    fvideos.close()
