#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This file runs SVM using a grid varying C and Gamma.
"""

import sys
sys.path.insert(0, '..')
import warnings
warnings.filterwarnings("ignore")
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import os
import argparse
from os.path import dirname, join, isdir

from classes import filehandler as fh
from models import classifier as clr

def main(filetrain, fileval, output, kernel, gamma_min, gamma_max, gamma_step, c_min, c_max, c_step):
    filetrain = fh.is_file(filetrain)
    fileval = fh.is_file(fileval)
    if output:
        dirout = fh.is_folder(output)
    else:
        dirin = dirname(filetrain)
        dirout = join(dirin, 'GridSVM')
        if not isdir(dirout):
            os.makedirs(dirout)
    clr.grid_svm(filetrain, fileval, dirout, kernel=kernel, 
             gamma_min=gamma_min, gamma_max=gamma_max, gamma_step=gamma_step,
             c_min=c_min, c_max=c_max, c_step=c_step)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filetrain', metavar='file_train', 
                        help='file containing training examples')
    parser.add_argument('fileval', metavar='file_validation', 
                        help='file containing validation examples')
    parser.add_argument('-o', '--output', help='Folder to store all results', default=None)
    parser.add_argument('-k', '--kernel', help='Type of kernel (based on scikit learn)', default='rbf')
    parser.add_argument('-g', '--gamma_min', help='Minimum value of Gamma', default=2e-15, type=float)
    parser.add_argument('-G', '--gamma_max', help='Maximum value of Gamma', default=2e3, type=float)
    parser.add_argument('-s', '--gamma_step', help='Step to multiply Gamma', default=1e2, type=float)
    parser.add_argument('-c', '--c_min', help='Minimum value of C', default=2e-5, type=float)
    parser.add_argument('-C', '--c_max', help='Maximum value of C', default=2e15, type=float)
    parser.add_argument('-S', '--c_step', help='Step to multiply C', default=1e2, type=float)
    args = parser.parse_args()

    main(args.filetrain, args.fileval, args.output, args.kernel,
         args.gamma_min, args.gamma_max, args.gamma_step, 
         args.c_min, args.c_max, args.c_step)



