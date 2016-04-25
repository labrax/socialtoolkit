#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

from .evolution_algorithm import EvolutionAlgorithm
from .centola import get_new_neighbor
from ..analysis.util import overlap_similarity, get_different_trait_index

from math import sqrt

import numpy.random as random
from random import choice

import networkx as nx

class ExpandableAlgorithm(EvolutionAlgorithm):
    def __init__(self, G, population, condition_axelrod, condition_centola):
        super(ExpandableAlgorithm, self).__init__(G, population)
        self._overlap_function = overlap_similarity
        self._post_args = None
        self.condition_axelrod = condition_axelrod
        self.condition_centola = condition_centola
    def iterate(self):
        ret = super(ExpandableAlgorithm, self).pre_iteration()
        if(ret == None):
            return None
        active, passive, neighbors, features_active, features_passive = ret
        params = [features_active, features_passive]
        if self._post_args:
            params += self._post_args
        s = self._overlap_function(*params)
        if self.condition_axelrod:
            if self.__condition_axelrod(s, features_active, features_passive):
                return True
        if self.condition_centola:
            if self.__condition_centola(s, active, passive, neighbors):
                return True
    def overlap_function(self, function, post_args):
        self._overlap_function = function
        self._post_args = post_args
    def __condition_axelrod(self, s, features_active, features_passive):
        if s > 0 and s < 1:
            if random.random() < s:
                i =  get_different_trait_index(features_active, features_passive)
                features_active[i] = features_passive[i]
                return True
    def __condition_centola(self, s, active, passive, neighbors):
        if s == 0.0:
            self.G.remove_edge(active, passive)
            new_neighbor = get_new_neighbor(self._all_nodes, set(neighbors))
            self.G.add_edge(active, new_neighbor)
            return True

class MultilayerAxelrod(ExpandableAlgorithm):
    def __init__(self, G, population):
        super(MultilayerAxelrod, self).__init__(G, population, True, False)

class MultilayerCentola(ExpandableAlgorithm):
    def __init__(self, G, population):
        super(MultilayerCentola, self).__init__(G, population, True, True)
