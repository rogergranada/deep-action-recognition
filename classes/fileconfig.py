#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
This script deals with the configuration file ``datasets.conf``
"""
import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class Configuration(object):

    def __init__(self, configfile=None):
        self.input = None
        self.color_id = []
        self.color_hx = []
        self.color_nm = [] 
        self.actions = {}     

        if configfile:
            self.input = open(configfile)
        else:
            self.input = open('../datasets.conf')
        self._loadcontent()

    
    def _loadcontent(self):
        for line in self.input:
            line = line.strip()
            if not line and line.startswith('#'):
                continue

            # General content
            if line.startswith('COLOR_HX'):
                line = line.replace('COLOR_HX = ', '')
                self.color_hx = [word.strip() for word in line.split(', ')]
            if line.startswith('COLOR_NM'):
                line = line.replace('COLOR_NM = ', '')
                self.color_nm = [word.strip() for word in line.split(', ')]
            if line.startswith('COLOR_ID'):
                line = line.replace('COLOR_ID = ', '')
                self.color_id = [int(word.strip()) for word in line.split(', ')]

            # Specific datasets
            if line.startswith('ACT_'):
                line = line.replace('ACT_', '')
                dataset, arr = line.split(' = ')
                actions = [word.strip() for word in arr.split(', ')]
                self.actions[dataset.strip().lower()] = actions

            # Generate alias
            if line.startswith('ALIAS_'):
                line = line.replace('ALIAS_', '')
                dataset, arr = line.split(' = ')
                dataset = dataset.strip().lower()
                alias = [word.strip() for word in arr.split(', ')]
                for alias_name in alias:
                    self.actions[alias_name.lower()] = self.actions[dataset]


    def labels(self, dataset):
        """
        Return the labels of ``dataset`` and their respective colors and ids
        """
        dataset = dataset.lower()
        if not self.actions.has_key(dataset):
            logger.error('Dataset %s does not exist!' % dataset)
            sys.exit(0)
        labels = self.actions[dataset]
        return labels


    def labels_colors(self, dataset):
        """
        Return the labels of ``dataset`` and their respective colors and ids
        """
        if not self.actions.has_key(dataset.lower()):
            logger.error('Dataset %s does not exist!' % dataset)
            sys.exit(0)
        labels = self.actions[dataset]
        colors = self.color_hx[:len(labels)]
        ids = self.color_id[:len(labels)]
        return labels, ids, colors


    def close(self):
        if self.input:
            self.input.close()
# End of class Configuration
