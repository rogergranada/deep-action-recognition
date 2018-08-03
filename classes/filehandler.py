#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import linecache
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import ast
import numpy as np
from os.path import realpath, dirname, splitext
from os.path import basename, isfile, isdir, join

from classes import progressbar
import fileconfig


def is_file(inputfile, boolean=False):
    """ Check whether the ``inputfile`` corresponds to a file """
    inputfile = realpath(inputfile)
    if not isfile(inputfile):
        if boolean:
            return False
        logger.error('Input is not a file!')
        sys.exit(0)
    return inputfile


def is_folder(inputfolder, boolean=False):
    """ Check whether the ``inputfolder`` corresponds to a folder """
    inputfolder = realpath(inputfolder)
    if not isdir(inputfolder):
        if boolean:
            return False
        logger.error('Argument %s is not a folder!' % inputfolder)
        sys.exit(0)
    return inputfolder


def add_text2path(path, text, withfolder=True):
    """ Add text to the end of the pathfile -- before the extension """
    path = realpath(path)
    dirfile = dirname(path)
    fname, ext = splitext(basename(path))
    fileout = fname+"_"+str(text)+ext
    if withfolder:
        return join(dirfile, fileout)
    return fileout


def filename(path, extension=True):
    fname, ext = splitext(basename(path))
    if extension:
        return fname, ext
    return fname


def add2dic(dic, key, value):
    if dic.has_key(key):
        dic[key].append(value)
    else:
        dic[key] = [value]
    return dic



def pairs_of_paths(vpaths, window):
    """
    Return pairs of images to generate the optical flow.
    These pairs contains the first and the last image of the optical flow
    according to the size of the window.
    
    Parameters:
    -----------
    vpaths : array_like
        sorted list containing the image ids (type int)
    window : int
        size of the window to generate the optical flow

    Returns:
    --------
    pairs : array_like
        list containing tuples with pairs as (first image, last image)
        of the optical flow

    Usage:
    ------
    >>> vpaths = [0, 1, 2, 3]
    >>> window_optical_flow(vpaths, 2)
        [(0, 2), (1, 3), (2, 3), (3, 3)]
    """
    pairs = []
    for img in vpaths:
        last_img = img + window
        if last_img in vpaths:
            pairs.append((img, last_img))
        else:
            pairs.append((img, vpaths[-1]))
    return pairs


class PathfileHandler(object):
    """Class to deal with files containing paths and labels/features"""

    def __init__(self, inputfile, display=True, load=False):
        """Initializes the class
        
        Parameters
        ----------
        inputfile : string
            path to the file containing images and labels/features
        display : boolean
            show the progress bar
        """
        self.display = display
        self.inputfile = realpath(inputfile)
        self.inputdir = dirname(inputfile)
        self.nb_lines = self.count_lines(inputfile)
        self.path = None
        self.label = None
        self.feats = None
        logger.debug('Loading file: %s' % inputfile)

        if load:
            self.vpaths, self.vlabels, self.vfeats = self.load_file(inputfile)


    def __iter__(self):
        """Iterates the file yielding the path, the true label and a vector of 
        features when exists
        """
        pb = progressbar.ProgressBar(self.nb_lines)
        with open(self.inputfile) as fin:
            for self.k, line in enumerate(fin):
                arr = self.split_line(line)
                if len(arr) == 1:
                    self.path = arr[0]
                    yield self.path
                if len(arr) == 2:
                    self.path, self.label = arr
                    yield self.path, self.label
                elif len(arr) == 3:
                    self.path, self.label, self.feats = arr
                    yield self.path, self.label, self.feats
                if self.display:
                    pb.update()


    @staticmethod
    def load_file(inputfile):
        """ Load the content of pathfile into `path`, `label` and `feats`
        """
        logger.debug('Loading file: %s' % inputfile)
        vpaths, vlabels, vfeats = [], [], []
        with open(inputfile) as fin:
            for line in fin:
                arr = line.strip().split()
                if len(arr) == 2:
                    vpaths.append(arr[0])
                    vlabels.append(int(arr[1]))
                elif len(arr) == 3:
                    vpaths.append(arr[0])
                    vlabels.append(int(arr[1]))
                    vfeats.append(int(arr[2]))
                elif len(arr) > 3:
                    vpaths.append(arr[0])
                    vlabels.append(int(arr[1]))
                    vfeats.append(map(float, arr[2:]))
        return vpaths, vlabels, vfeats


    @staticmethod
    def count_lines(inputfile):
        """ Returns the total number of images in the input file 

        Parameters
        ----------
        inputfile : string
            path to the file containing images and labels/features

        Returns
        -------
        n : int
            total number of lines in the document
        """
        with open(inputfile) as fin:
            for n, _ in enumerate(fin, start=1): pass
        return n


    @staticmethod
    def split_line(line, text=False):
        """
        Split line into path, true label and features.
        
        Parameters:
        -----------
        line: string
            line with at least `path`
        text: boolean
            return `feats` in text form instead of a list
        """
        arr = line.strip().split()
        if len(arr) == 1:
            path = arr
            return path
        elif len(arr) > 1:
            path = arr[0]
            label = arr[1]
            if len(arr) > 2:
                if text:
                    feats = ' '.join(arr[2:])
                elif len(arr[2:]) == 1:
                    feats = ast.literal_eval(arr[2])
                else:
                    feats = map(float, arr[2:])
                return path, label, feats
            else:
                return path, label


    def get_line(self, nb_line):
        """Returns the line at number `nb_line`"""
        return linecache.getline(self.inputfile, nb_line).strip()


    def get_path(self, nb_line, label=False):
        """Returns the path of the line at number `nb_line`"""
        line = linecache.getline(self.inputfile, nb_line)
        path = None
        if line:
            arr = line.split()
            path = arr[0]
            if label:
                y = arr[1]
                return path, y
        return path


    def get_label(self, nb_line):
        """Returns the path of the line at number `nb_line`"""
        line = linecache.getline(self.inputfile, nb_line)
        label = None
        if line:
            label = line.split()[1]
        return label


    def features_line(self, nb_line, asstr=False):
        """Returns only the feature of the line number `nb_line`"""
        line = linecache.getline(self.inputfile, nb_line)
        arr = line.strip().split()
        if len(arr) > 2:
            if asstr:
                return ' '.join(arr[2:])
            else:
                return arr[2:]
        return None


    def current_features(self, N=2):
        """
        Return a list containing the `N` features with the highest scores

        Parameters:
        -----------
        N : int
            number of features to return

        Notes:
        ------
        The output has the form of a list as:
        [(1, 0.33), (3, 0.12), (5, 0.08), ...]
        """
        features = self.labels[1:]
        classes = map(int, features[0::2])
        preds = np.array(features[1::2], dtype=np.float32)
        topN = []
        for n in range(N):
            valmax = preds.max()
            imax = preds.argmax()
            topN.append((classes[imax], valmax))
            preds[imax] = -1
        return topN


    def has_features(self):
        """
        Returns
        -------
        _ : bool
            False : only path and label
            True : path, label and features
        """
        line = self.get_line(1)
        arr = line.strip().split()
        if len(arr) > 2:
            return True
        else:
            return False
#End of class PathfileHandler


class Videos(PathfileHandler):
    """ Class to extract videos from files """

    def __init__(self, inputfile, dataset):
        PathfileHandler.__init__(self, inputfile, display=False)
        self.videos = {}
        self.root = None
        self.ext = None
        cfg = fileconfig.Configuration()
        self.name = cfg.has_dataset(dataset)


    def _videos_dogs(self, nb_frames=False):
        # ~/Car/Car_Ringo_5_9810_9910_frame_83.jpg
        fname, self.ext = splitext(basename(self.path))
        nm_video, frame = fname.split('_frame_')
        self.root = nm_video+'_frame_'
        if nb_frames:
            frame = int(frame)
            return nm_video, frame
        else:
            return nm_video, self.path


    def _videos_kscgr(self, nb_frames=False):
        # ~/Data/data1/boild-egg/img256/0.jpg
        arr = self.path.split('/')
        self.root = '/'.join(arr[:-4])
        nm_video = arr[-4]+'_'+arr[-3]+'_'+arr[-2]
        if nb_frames:
            frame, self.ext = splitext(basename(self.path))
            frame = int(frame)
            return nm_video, frame
        else:
            return nm_video, self.path


    def _videos_ucf11(self, nb_frames=False):
        # ~/basketball/v_shooting_14/v_shooting_14_01/image_00001.jpg
        arr = self.path.split('/')
        self.root = '/'.join(arr[:-4])
        nm_video = arr[-4]+'_'+arr[-3]+'_'+arr[-2]
        if nb_frames:
            frame, self.ext = splitext(basename(self.path))
            frame = int(frame.split('_')[1])
            return nm_video, frame
        else:
            return nm_video, self.path


    def _videos_penn(self, nb_frames=False):
        # ~/frames/0001/000001.jpg
        arr = self.path.split('/')
        self.root = '/'.join(arr[:-2])
        nm_video = arr[-2]
        if nb_frames:
            frame, self.ext = splitext(basename(self.path))
            return nm_video, frame
        else:
            return nm_video, self.path


    def _video_frame(self, nb_frames=False):
        """ Return the name of the video and the number of the frame """
        if self.name == "dogs":
            videoframes = self._videos_dogs(nb_frames)
        elif self.name == "kscgr":
            videoframes = self._videos_kscgr(nb_frames)
        elif self.name == "ucf11":
            videoframes = self._videos_ucf11(nb_frames)
        elif self.name == "penn":
            videoframes = self._videos_penn(nb_frames)
        else:
            videoframes = None, None
        return videoframes


    def extract_videos(self):
        """ Create a dictionary containing {video_name: [frames]} """
        for k in self:
            nm_video, frame = self._video_frame()
            add2dic(self.videos, nm_video, int(frame))
        return self.videos


    def label_videos(self):
        """ 
        Creates a dictionary containing the class of the video as the key
        and a dictionary with the name of video and frames as value.
        The dictionary has the structure of:
            dic[label] = {path_to_image: [image_names]}
        Thus, the examples below become:
            /usr/share/datasets/Penn_Action/256/frames/0001/000001.jpg 0
            /usr/share/datasets/Penn_Action/256/frames/0001/000002.jpg 0

            dic[0] = {'/usr/share/datasets/Penn_Action/256/frames/0001':
                        ['000001.jpg', '000002.jpg, ... '000049.jpg'],
                      '/usr/share/datasets/Penn_Action/256/frames/0002':
                        ['000001.jpg', '000002.jpg, ... '000049.jpg']
            }
        """
        for _ in self:
            nm_video, frame = self._video_frame(nb_frames=True)
            fvideo = join(self.root, nm_video)
            label = int(self.label)

            if self.videos.has_key(label):
                add2dic(self.videos[label], fvideo, (frame))
            else:
                self.videos[label] = {fvideo: [frame]}
        return self.videos
#End of class Videos


class ImagePaths(PathfileHandler):
    """ Class to deal with names of paths """

    def __init__(self, inputfile, dataset, display=False):
        PathfileHandler.__init__(self, inputfile, display=display)
        self.root = None
        self.fname = None
        self.ext = None
        cfg = fileconfig.Configuration()
        self.name = cfg.has_dataset(dataset)


    def _paths_dogs(self):
        # ~/Car/Car_Ringo_5_9810_9910_frame_83.jpg
        arr = self.path.split('/')
        self.root = '/'.join(arr[0:-2])
        self.fname = '/'.join(arr[-2:])
        _, self.ext = splitext(basename(self.path))


    def _paths_penn(self):
        # ~/frames/0001/000005.jpg
        arr = self.path.split('/')
        self.root = '/'.join(arr[0:-3])
        self.fname = '/'.join(arr[-3:])
        _, self.ext = splitext(basename(self.path))


    def _paths_kscgr_ucf11(self):
        # ~/data1/boild-egg/img256/0.jpg
        # ~/basketball/v_shooting_14/v_shooting_14_01/image_00001.jpg
        arr = self.path.split('/')
        self.root = '/'.join(arr[0:-4])
        self.fname = '/'.join(arr[-4:])
        _, self.ext = splitext(basename(self.path))


    def extract_root(self):
        """ extract the root and file name of paths """
        if self.name == "dog":
            self._paths_dogs()
        elif self.name in ("kscgr", "ucf11"):
            self._paths_kscgr_ucf11()
        elif self.name == "penn":
            self._paths_penn()
        return self.root, self.fname
#End of class ImagePaths


def check_sizefiles(file1, file2, warning=False):
    """
    Verify whether both files have the same number of lines.
    """
    nb_1 = PathfileHandler.count_lines(file1)
    nb_2 = PathfileHandler.count_lines(file2)
    if nb_1 != nb_2:
        logger.error('Number of lines are different in %s and %s (%d:%d)' % 
                     (file1, file2, nb_1, nb_2))
        if not warning:
            sys.exit(0)
    if nb_1 < nb_2:
        return nb_1
    return nb_2


def change_paths(gt_file, ft_file, outfile):
    """
    Change the paths of the file containing features with the paths
    of the ground truth file.

    Parameters:
    -----------
    gt_file: string
        path to the file containing paths and ground truth
    ft_file: string
        path to the file containing extracted features. 
        The content in output is saved in this file 
    outfile: string
        path to the file that will contain the new paths
    """
    gt_file = is_file(gt_file)
    ft_file = is_file(ft_file)
    dirin = dirname(ft_file)
    nb_gt = check_sizefiles(gt_file, ft_file)

    fout = open(join(dirin, outfile), 'w')
    logger.info('Reading files...')
    pb = progressbar.ProgressBar(nb_gt)
    with open(gt_file) as fgt, open(ft_file) as fft:
        for lgt, lft in zip(fgt, fft):
            path_new = lgt.strip().split()[0]
            path_old = lft.strip().split()[0]
            lft = lft.replace(path_old, path_new)
            fout.write(lft)
            pb.update()
    fout.close()


def load_features(inputfile):
    """
    From a file with the path of images, true labels and features
    return the features and true labels.

    Parameters:
    -----------
    inputfile: string
        path to the file containing paths, true labels and features
    """
    pf = PathfileHandler(inputfile, load=True)
    X = np.array(pf.vfeats).astype(float)
    y = np.array(pf.vlabels).astype(int)
    return pf.vpaths, X, y

def merge_features(feats1, feats2, mean=False):
    """
    Function to merge `feats1`and `feats2` features into a single line.
    By default the merging is performed by concatenating, but setting
    the `mean` flag, features are merged by the average of their values.
    """
    if mean:
        feats1 = np.array(map(float, feats1[2:]))
        feats2 = np.array(map(float, feats2[2:]))
        vmean = (feats1+feats2)/2.
        feats = ' '.join(map(str, vmean))
    else:
        feats1 = ' '.join(map(str, feats1))
        feats2 = ' '.join(map(str, feats2))
        feats = feats1+' '+feats2
    return feats


def merge_features_equal_files(file1, file2, fileout, mean=False):
    """
    Given two files containing paths, true labels and features the function
    merges both files into a single file containing paths, true labels and 
    the concatenation or the mean of the features.

    Obs. when two files have different number of features, a warning appears.
    This case may occur when trying to concatenate raw RGB images and optical
    flow images, since the last image in optical flow is not generated.
    
    Parameters:
    -----------
    file1 : string
        path to the input file
    file2 : string
        path to the input file
    fileout : string
        path to the output file
    mean: boolean
        generate the mean of the features instead of the concatenation
    """
    nb_lines = check_sizefiles(file1, file2, warning=True)
    logger.info('Recording output file: %s' % fileout)
    fout = open(fileout, 'w')

    logger.info('Reading files...')
    pb = progressbar.ProgressBar(nb_lines)
    id_line = 1
    with open(file1) as fin1, open(file2) as fin2:
        for l1, l2 in zip(fin1, fin2):
            arr1 = l1.strip().split()
            fname1 = basename(arr1[0])
            feats1 = arr[2:]
            
            arr2 = l2.strip().split()
            fname2 = basename(arr2[0])
            feats2 = arr[2:]
            
            if fname1 != fname2:
                logger.error('Trying to merge different images (%s : %s) : reading line (%d)' % (fname1, fname2, id_line))
                logger.error('Error while reading line: %d' % id_line)
                logger.error('Try merge_features_different_files() instead')
                sys.exit(0)
            feats = merge_features(feats1, feats2, mean=mean)
            fout.write('%s %s %s\n' % (arr1[0], arr1[1], feats))
            id_line += 1
            pb.update()
    fout.close()


def imgpath2dic(inputfile, dataset, id=True, filename=False):
    """ Create a dictionary containing an index for each path in a file """
    inputfile = is_file(inputfile)
    pf = ImagePaths(inputfile, dataset, display=True)
    dic = {}
    for _ in pf:
        if id:
            dic[pf.k+1] = pf.path
        else:
            if filename:
                _, fname = pf.extract_root()
                dic[fname] = pf.k+1
            else:
                dic[pf.path] = pf.k+1
    return dic


def merge_features_different_files(file1, file2, fileout, dataset, mean=False, inverse=False):
    """
    Merge two files where the features are in different order. Use the first
    file as reference or the second using `inverse`.
    This function should be used only when the user knows that features are scrambled
    or missing.

    Parameters:
    -----------
    file1 : string
        path to the input file
    file2 : string
        path to the input file
    fileout : string
        path to the output file
    mean: boolean
        generate the mean of the features instead of the concatenation
    inverse: boolean
        use the first or the second file as reference (inverse=False : 1st file)
    """
    logger.info('Recording output file: %s' % fileout)
    fout = open(fileout, 'w')
    if inverse:
        frefs = file2
        ffeat = file1
    else:
        frefs = file1
        ffeat = file2

    dfeat = imgpath2dic(ffeat, dataset, id=False, filename=True)
    pfh = PathfileHandler(ffeat, display=False)

    pf = ImagePaths(frefs, dataset, display=True)
    for path, label, featsref in pf:
        _, fname = pf.extract_root()
        featsref = ' '.join(map(str, featsref))
        if dfeat.has_key(fname):
            nb_line = dfeat[fname]
            line = pfh.get_line(nb_line)
            _, _, feats = pfh.split_line(line, text=True)
            fout.write('%s %s %s %s\n' % (path, label, featsref, feats))
    fout.close() 
