#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This source defines the basic evolution algorithm, expanded for the models of Axelrod and Centola, and those multilayer.
"""

from ..algorithm import Algorithm

import networkx as nx

from math import sqrt
from numpy import random
from random import choice

class EvolutionAlgorithm(Algorithm):
    """Base algorithm for evolution"""
    def __init__(self, G, population):
        """Initiates the algorithm collecting basic information.
        
        Args:
            G (networkx.classes.graph): the graph.
            population (list of list): the features and traits of the population."""
        self.G = G
        self.population = population
        self._nodes = len(population)
        self._features = len(population[0])
        self._all_nodes = list(G.nodes())
        if nx.info(G).split('\n')[0][6:] == 'grid_2d_graph':
            self._grid = True
        else:
            self._grid = False
    def getName(self):
        """Returns self.__class__.__name__"""
        return self.__class__.__name__
    def pre_iteration(self):
        """Returns pre information for one iteration: active node, passive node, neighbors of active, features of active node and features of passive node"""
        if self._grid:
            active = (int(sqrt(random.randint(self._nodes))), int(sqrt(random.randint(self._nodes))))
            neighbors = self.G.neighbors(active)
            if len(neighbors) == 0:
                return None
            passive = choice(neighbors)
            features_active = self.population[active[0]*int(sqrt(self._nodes)) + active[1]]
            features_passive = self.population[passive[0]*int(sqrt(self._nodes)) + active[1]]
            return (active, passive, neighbors, features_active, features_passive)
        else:
            active = random.randint(self._nodes)
            neighbors = self.G.neighbors(active)
            if len(neighbors) == 0:
                return None
            passive = choice(neighbors)
            features_active = self.population[active]
            features_passive = self.population[passive]
            return (active, passive, neighbors, features_active, features_passive)
    def iterate(self):
        """Dummy: do nothing - to be implemented on children classes"""
        pass
