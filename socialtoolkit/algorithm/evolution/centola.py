#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

from .evolution_algorithm import EvolutionAlgorithm
from ..analysis.util import overlap_similarity, get_different_trait_index

import numpy.random as random
from random import choice

import networkx as nx

class Centola(EvolutionAlgorithm):
    def __init__(self, G, population):
        super(Centola, self).__init__(G, population)
    def iterate(self):
        active, passive, neighbors, features_active, features_passive = super(Centola, self).pre_iteration()
        s = overlap_similarity(features_active, features_passive)
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
        
def get_new_neighbor(G, neighbors):
    """get a node from graph that isn't in neighbours: this method supposes that graph is always greater than neighbours"""
    while True:
        test_case = G[random.randint(len(G))]
        if test_case not in neighbors:
            return test_case
