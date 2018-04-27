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


def main(input_1, dataset_1, input_2, dataset_2, input_3, dataset_3, output=None, values=False):
    input_1 = filehandler.is_file(input_1)
    input_2 = filehandler.is_file(input_2)
    input_3 = filehandler.is_file(input_3)

    if output:
        fname = output
        _, ext = filehandler.filename(output, extension=True)
        ext = ext.replace('.', '')
    else:
        dirout = dirname(input_1)
        fname = join(dirout, 'cm.eps')
        ext = 'eps'

    mats = []
    cm_1 = plots.ConfusionMatrix(dataset_1, inputfile=input_1) 
    mats.append(cm_1._genConfusionMatrix())
    cm_2 = plots.ConfusionMatrix(dataset_2, inputfile=input_2)
    mats.append(cm_2._genConfusionMatrix())
    cm_3 = plots.ConfusionMatrix(dataset_3, inputfile=input_3)
    mats.append(cm_3._genConfusionMatrix())

    titles = [dataset_1, dataset_2, dataset_3]
    vec_labels = [cm_1.labels, cm_2.labels, cm_3.labels]
    plots.save_multiple_plots(fname, mats, vec_labels, title=titles, cmap=plt.cm.Blues, type=ext, show_values=values)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_1', metavar='file_input_1', help='File containing paths to images and true labels')
    parser.add_argument('dataset_1', metavar='dataset_1', help='Name of the dataset to plot the confusion matrix')
    parser.add_argument('input_2', metavar='file_input_2', help='File containing paths to images and true labels')
    parser.add_argument('dataset_2', metavar='dataset_2', help='Name of the dataset to plot the confusion matrix')
    parser.add_argument('input_3', metavar='file_input_3', help='File containing paths to images and true labels')
    parser.add_argument('dataset_3', metavar='dataset_3', help='Name of the dataset to plot the confusion matrix')
    parser.add_argument('-o', '--output', help='File to save the confusion matrix', default=None)
    parser.add_argument('-v', '--values', help='Show values in confusion matrix', action='store_true')
    args = parser.parse_args()

    main(args.input_1, args.dataset_1, args.input_2, args.dataset_2, 
         args.input_3, args.dataset_3, output=args.output, values=args.values)
