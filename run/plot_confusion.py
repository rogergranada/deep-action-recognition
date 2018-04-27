#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
This script plots the confusion matrix of a file containing paths, true labels and predicted labels
"""
import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import os
import argparse
from os.path import dirname, join, exists
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# customized files
from classes import filehandler, plots


def main(inputfile, dataset, output=None, values=False):
    inputfile = filehandler.is_file(inputfile)
    if output:
        fname = output
        _, ext = filehandler.filename(output, extension=True)
        ext = ext.replace('.', '')
    else:
        dirout = dirname(inputfile)
        fname = join(dirout, 'cm.eps')
        ext = 'eps'

    cm = plots.ConfusionMatrix(dataset, inputfile=inputfile) 
    cm.save_plot(fname, title='', cmap=plt.cm.Blues, type=ext, show_values=values)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', metavar='file_input', help='File containing paths to images and true labels')
    parser.add_argument('dataset', metavar='dataset', help='Name of the dataset to plot the confusion matrix')
    parser.add_argument('-o', '--output', help='File to save the confusion matrix', default=None)
    parser.add_argument('-v', '--values', help='Show values in confusion matrix', action='store_true')
    args = parser.parse_args()

    main(args.inputfile, args.dataset, output=args.output, values=args.values)
