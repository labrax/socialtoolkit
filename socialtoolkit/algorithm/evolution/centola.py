#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This source defines the Centolas's algorithm for cultural drift and diffusion.
"""

from .evolution_algorithm import EvolutionAlgorithm
from ..analysis.util import overlap_similarity, get_different_trait_index

import numpy.random as random


class Centola(EvolutionAlgorithm):
    """Algorithm for evolution as proposed on Centola's paper for cultural drift and diffusion"""
    def __init__(self, G, population):
        """Initiates the algorithm with default settings.
        
        Args:
            G (networkx.classes.graph): the graph.
            population (list of list): the features and traits of the population."""
        super(Centola, self).__init__(G, population)

    def iterate(self):
        """Iterate once using this algorithm"""
        active, passive, neighbors, features_active, features_passive = super(Centola, self).pre_iteration()
        s = overlap_similarity(features_active, features_passive)
        if 0 < s < 1:
            if random.random() < s:
                i = get_different_trait_index(features_active, features_passive)
                features_active[i] = features_passive[i]
                return True
        elif s == 0.0:
            self.G.remove_edge(active, passive)
            new_neighbor = get_new_neighbor(self._all_nodes, set(neighbors))
            self.G.add_edge(active, new_neighbor)
            return True


def get_new_neighbor(G, neighbors):
    """Returns a node from the graph that isn't in neighbors:
    this method supposes that graph is always greater than neighbours.
    
    Args:
        G (networkx.classes.graph): the graph.
        neighbors (list): list of neighbors from a node."""
    while True:
        test_case = G[random.randint(len(G))]
        if test_case not in neighbors:
            return test_case
