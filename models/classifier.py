#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
This file contains functions to employ classifiers such as SVM.
"""

import sys
sys.path.insert(0, '..')
import warnings
warnings.filterwarnings("ignore")
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from sklearn import svm

from classes import filehandler as fh

def create_range(vmin, vmax, step):
    """ 
    Create a geometric progression with from `vmin` to `vmax`
    using `step` as multiplier.
    """
    vrange = []
    val = vmin
    while val <= vmax:
        vrange.append(val)
        val *= step
    return vrange


def grid_svm(trainfile, valfile, outputdir, kernel='rbf', 
             gamma_min=2e-15, gamma_max=2e3, gamma_step=1e2,
             c_min=2e-5, c_max=2e15, c_step=1e2):
    """
    Perform a grid of parameters in SVM

    Parameters:
    -----------
    trainfile: string
        path to the file containing training features
    valfile: string
        path to the file containing validation features
    outputdir: string
        path to the folder to save tests
    kernel: string
        type of kernel (scikit names)
    gamma_min: int
        minimum value of gamma
    gamma_max: int
        maximum value of gamma
    gamma_step: int
        step of increasing gamma
    c_min: int
        minimum value of C
    c_max: int
        maximum value of C
    c_step: int
        step of increasing value of C
    """
    trainfile = fh.is_file(trainfile)
    _, X_train, y_train = fh.load_features(trainfile)
    valfile = fh.is_file(valfile)
    vpaths, X_val, y_val = fh.load_features(valfile)
    outputdir = fh.is_folder(outputdir)

    vgamma = create_range(gamma_min, gamma_max, gamma_step)
    vc = create_range(c_min, c_max, c_step)
    svc = svm.SVC(kernel=kernel, verbose=True)
    for c in vc:
        for g in vgamma:
            logger.info('Running C: %E :: Gamma: %E' % (c, g))
            clf = svm.SVC(kernel=kernel, C=c, gamma=g)
            clf.fit(X_train, y_train)
            pred = clf.predict(X_val)

            fileout = join(outputdir, kernel+'_'+str(c)+'_'+str(g)'.txt')
            logger.info('saving output file in: %s' % fileout)
            with open(fileout, 'w') as fout:
                for path, y, p in zip(vpaths, y_val, pred):
                    fout.write('%s %d %d\n' % (path, y, p))
    logger.info('Finished!')
