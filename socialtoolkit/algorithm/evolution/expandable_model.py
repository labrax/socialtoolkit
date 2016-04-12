#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

from evolution_algorithm import EvolutionAlgorithm
from centola import get_new_neighbor
from ..analysis.util import overlap_similarity, get_different_trait_index

from math import sqrt

import numpy.random as random
from random import choice

import networkx as nx

class ExpandableAlgorithm(EvolutionAlgorithm):
    def __init__(self, G, population):
        super(ExpandableAlgorithm, self).__init__(G, population)
        self._overlap_function = overlap_similarity
        self._post_args = None
    def iterate(self):
        ret = super(ExpandableAlgorithm, self).pre_iteration()
        if(ret == None):
            return None
        active, passive, neighbors, features_active, features_passive = ret
        params = [features_active, features_passive]
        if self._post_args:
            params += self._post_args
        s = self._overlap_function(*params)
        if s > 0 and s < 1:
            if random.random() < s:
                i =  get_different_trait_index(features_active, features_passive)
                features_active[i] = features_passive[i]
                return True
        elif s == 0.0:
            self.G.remove_edge(active, passive)
            new_neighbor = get_new_neighbor(self._all_nodes, set(neighbors))
            self.G.add_edge(active, new_neighbor)
            return True
    def overlap_function(self, function, post_args):
        self._overlap_function = function
        self._post_args = post_args

