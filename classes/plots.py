#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This file contains classes for plotting true labels and predicted labels.
"""
import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import itertools
from sklearn.metrics import confusion_matrix
from os.path import join, splitext, basename, realpath, dirname
from collections import Counter

# customized files
from classes import filehandler, fileconfig


class ConfusionMatrix(object):
    
    def __init__(self, dataset, inputfile=None, cmatrix=None):
        """
        Parameters:
        -----------
        dataset : string
            name of the dataset to be loaded from ``datasets.conf``
        inputfile : string
            path to the file containing true labels and predicted labels
        cmatrix : sklearn.metrics.confusion_matrix
            the confusion matrix to generate the plot
        """
        self.cm = None
        self.vlabel, self.vpred = [], []

        fc = fileconfig.Configuration()
        self.labels = fc.labels(dataset)

        if cmatrix:
            self.cm = cmatrix
        elif inputfile:
            fh = filehandler.PathfileHandler(inputfile)
            vlabel, vpred = [], []
            for arr in fh:
                if len(arr) == 3:
                    _, label, pred = arr[0], arr[1], arr[2]
                    vlabel.append(label)
                    vpred.append(pred)
            self.vlabel = np.array(vlabel, dtype=float)
            self.vpred = np.array(vpred, dtype=float)


    def _genConfusionMatrix(self):
        """
        Build the confusion matrix
        """
        if not self.cm:
            self.cm = confusion_matrix(self.vlabel, self.vpred)
        sum_col = self.cm.sum(axis=1)[:, np.newaxis]
        with np.errstate(divide='ignore', invalid='ignore'):
            cm_norm = np.true_divide(self.cm.astype('float'), sum_col)
            cm_norm[~ np.isfinite(cm_norm)] = 0  # -inf inf NaN
        return cm_norm


    def save_plot(self, fname, title='', cmap=plt.cm.Blues, type='eps', show_values=False):
        """
        Save the confusion matrix into a file `fname`

        Parameters:
        -----------
        fname : string
            path to the output file (with extension)
        title : string
            title of the plot
        cmap : pyplot colors
            colors of matplotlib
        type : string
            extension of the image file
        """
        logger.info('Saving confusion matrix: %s' % fname)
        plt.gcf().subplots_adjust(bottom=0.15)
        cm_norm = self._genConfusionMatrix()
        plt.imshow(cm_norm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(self.labels))
        plt.xticks(tick_marks, self.labels, rotation=45, ha='right', fontsize=12)
        plt.yticks(tick_marks, self.labels, fontsize=12)
    
        if show_values:
            thresh = cm_norm.max() / 2.
            for i, j in itertools.product(range(cm_norm.shape[0]), range(cm_norm.shape[1])):
                plt.text(j, i, format(cm_norm[i, j], '.2f'),
                     horizontalalignment="center", fontsize=5,
                     color="white" if cm_norm[i, j] > thresh else "black")

        #plt.tight_layout()
        #plt.ylabel('Predicted label')
        #plt.xlabel('True label')
        plt.savefig(fname, format=type)
#End of DisplayConfusionMatrix class

def save_multiple_plots(fname, matrices, vec_labels, title='', cmap=plt.cm.Blues, type='eps', show_values=False):
    """
    Save the multiple confusion matrices into a file `fname`

    Parameters:
    -----------
    fname : string
        path to the output file (with extension)
    title : array
        title of each plot
    cmap : pyplot colors
        colors of matplotlib
    type : string
        extension of the image file
    """ 
    if len(matrices) != len(vec_labels):
        logger.error("Titles and Matrices must have the same lenght")

    nbmats = len(matrices)
    subplts = '1'+str(nbmats)
    plt.figure(figsize=(35,10))

    plt.subplot(141)    
    plt.imshow(matrices[0], interpolation='nearest', cmap=cmap, aspect='auto')
    tick_marks = np.arange(len(vec_labels[0]))
    plt.xticks(tick_marks, vec_labels[0], rotation=45, ha='right', fontsize=16)
    plt.yticks(tick_marks, vec_labels[0], fontsize=16)
    plt.title(title[0])
    plt.subplot(142)    
    plt.imshow(matrices[1], interpolation='nearest', cmap=cmap, aspect='auto')
    tick_marks = np.arange(len(vec_labels[1]))
    plt.xticks(tick_marks, vec_labels[1], rotation=45, ha='right', fontsize=16)
    plt.yticks(tick_marks, vec_labels[1], fontsize=16)
    plt.title(title[1])
    plt.subplot(143)    
    plt.imshow(matrices[2], interpolation='nearest', cmap=cmap, aspect='auto')
    tick_marks = np.arange(len(vec_labels[2]))
    plt.xticks(tick_marks, vec_labels[2], rotation=45, ha='right', fontsize=16)
    plt.yticks(tick_marks, vec_labels[2], fontsize=16)
    plt.title(title[2])
    
    """
    logger.info('Saving confusion matrix: %s' % fname)
    index = 1
    for confmat, labels in zip(matrices, vec_labels):
        nbplot = int(subplts+str(index))
        plt.subplot(nbplot)
        #plt.ylabel('Damped oscillation')
        #plt.suptitle('This is a somewhat long figure title', fontsize=16)

        #plt.gcf().subplots_adjust(bottom=0.15)
        print confmat
        plt.imshow(confmat, interpolation='nearest', cmap=cmap)
        #plt.suptitle(title)

        if show_values:
            thresh = confmat.max() / 2.
            for i, j in itertools.product(range(confmat.shape[0]), range(confmat.shape[1])):
                plt.text(j, i, format(confmat[i, j], '.2f'),
                     horizontalalignment="center", fontsize=5,
                     color="white" if confmat[i, j] > thresh else "black")
        index += 1
    """
    plt.subplots_adjust(bottom=0.1, right=0.6, top=0.9)
    cax = plt.axes([0.75, 0.15, 0.02, 0.81])
    #plt.colorbar(cax=cax)
    bounds = np.linspace(0.0,1.0,11)
    print bounds
    cb = mpl.colorbar.ColorbarBase(cax, cmap=cmap, ticks=bounds) #, format='%1i')
    cb.ax.tick_params(labelsize=16) 

    #plt.colorbar()
    #plt.subplots_adjust(left=1, wspace=0.8, top=0.8)
    #plt.subplots_adjust(left=0.1, bottom = 0.1, top=0.9)

    plt.tight_layout()
    #plt.ylabel('Predicted label')
    #plt.xlabel('True label')
    plt.savefig(fname, format=type)
