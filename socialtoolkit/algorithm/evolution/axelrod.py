#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This source defines the Axelrod's algorithm for cultural diffusion.
"""

from .evolution_algorithm import EvolutionAlgorithm
from ..analysis.util import overlap_similarity, get_different_trait_index

import numpy.random as random
from random import choice

import networkx as nx

class Axelrod(EvolutionAlgorithm):
    """Algorithm for evolution as proposed on Axelrod's paper for cultural diffusion"""
    def __init__(self, G, population):
        """Initiates the algorithm with default settings.
        
        Args:
            G (networkx.classes.graph): the graph.
            population (list of list): the features and traits of the population."""
        super(Axelrod, self).__init__(G, population)
    def iterate(self):
        """Iterate once using this algorithm"""
        active, passive, neighbors, features_active, features_passive = super(Axelrod, self).pre_iteration()
        s = overlap_similarity(features_active, features_passive)
        if s > 0 and s < 1:
            if random.random() < s:
                i =  get_different_trait_index(features_active, features_passive)
                features_active[i] = features_passive[i]
                return True
