#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
This script deals with the configuration file ``datasets.conf``

In this script, actions are stored in a dictionary with the main key represented by
`ACT_<dataset>` in configuration file. Aliases to `<dataset>` are stored in another
dictionary where the value refers to `<dataset>` name. Thus, the dictionary of actions
may be composed as:

actions['dog'] = ['Car', 'Drink', 'Feed', 'Left', 'Right', 'Pet', 'Play', 'Shake', 'Sniff', 'Walk']

While the dictionary containing dataset may be composed as:

dataset = {'dogs': 'dog', 'dogcentric': 'dog'}
"""
import sys
sys.path.insert(0, '..')
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class Configuration(object):

    def __init__(self, configfile=None):
        self.fconf = configfile
        self.color_id = []
        self.color_hx = []
        self.color_nm = [] 
        self.actions = {}
        self.dataset = {}

        if configfile:
            self.input = open(configfile)
        else:
            self.fconf = '../datasets.conf'
            self.input = open('../datasets.conf')
        self._loadcontent()

    
    def __str__(self):
        """ Return the content of the class """
        content = 'File configuration: '+str(self.fconf)
        content += '\nColor IDs:'+str(self.color_id)
        content += '\nColor Hex:'+str(self.color_hx)
        content += '\nColor Names:'+str(self.color_nm)
        content += '\nActions:'+str(self.actions)
        return content

    
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
                self.dataset[dataset] = dataset
                alias = [word.strip() for word in arr.split(', ')]
                for alias_name in alias:
                    self.dataset[alias_name.lower()] = dataset


    def has_dataset(self, dataset, exit=True):
        """ Verify if the dataset exists """
        dataset = dataset.lower()
        if not self.dataset.has_key(dataset):
            logger.error('Dataset %s does not exist!' % dataset)
            if exit:
                sys.exit(0)
            else:
                return False
        return self.dataset[dataset]


    def labels(self, dataset):
        """
        Return the labels of ``dataset`` and their respective colors and ids
        """
        dataset = self.has_dataset(dataset)
        labels = self.actions[dataset]
        return labels


    def labels_colors(self, dataset):
        """
        Return the labels of ``dataset`` and their respective colors and ids
        """
        dataset = self.has_dataset(dataset)
        labels = self.actions[dataset]
        colors = self.color_hx[:len(labels)]
        ids = self.color_id[:len(labels)]
        return labels, ids, colors


    def id_label(self, dataset, key='label'):
        """
        Return each label with its ID associated
        """
        dataset = self.has_dataset(dataset)
        labels = self.actions[dataset]
        ids = self.color_id[:len(labels)]
        if key == 'label':
            dic = [(lbl.lower(), id) for lbl, id in zip(labels, ids)]
        else:
            dic = [(id, lbl.lower()) for lbl, id in zip(labels, ids)]
        return dict(dic)


    def close(self):
        if self.input:
            self.input.close()
# End of class Configuration
