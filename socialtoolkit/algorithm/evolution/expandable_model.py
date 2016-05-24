#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This source defines the multilayer algorithm for evolution, with both the Axelrod and Centola.
"""

from .evolution_algorithm import EvolutionAlgorithm
from .centola import get_new_neighbor
from ..analysis.util import overlap_similarity, get_different_trait_index

import numpy.random as random


class ExpandableAlgorithm(EvolutionAlgorithm):
    """Base expandable algorithm: optional function for overlap_similarity;
    optional conditions of Axelrod and Centola"""
    def __init__(self, G, population, condition_axelrod, condition_centola):
        """Initiates the algorithm with default overlap similarity function.
                
        Args:
            G (networkx.classes.graph): the graph.
            population (list of list): the features and traits of the population.
            condition_axelrod (bool): True to use the Axelrod condition.
            condition_centola (bool): True to use the Centola condition.
            
        Note:
            The Axelrod condition is for similarity between 0.0 and 1.0: pass a trait from the passive to active node.
            The Centola condition is for similarity equals to 0: removes the edge and connect to another node."""
        super(ExpandableAlgorithm, self).__init__(G, population)
        self._overlap_function = overlap_similarity
        self._post_args = None
        self.condition_axelrod = condition_axelrod
        self.condition_centola = condition_centola

    def iterate(self):
        """Iterate once using this algorithm"""
        ret = super(ExpandableAlgorithm, self).pre_iteration()
        if ret is None:
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
        """Modifies the function to be called for the similarity overlap.
        
        Args:
            function (function): the function to use as overlap_similarity.
            post_args (list): of arguments to be appended to features_active and features_passive on a check."""
        self._overlap_function = function
        self._post_args = post_args

    def __condition_axelrod(self, s, features_active, features_passive):
        """Test the conditions for similarity in between 0.0 and 1.0 - in axelrod it is the transfering of a random feature.
        
        Args:
            s (float): the similarity between two nodes.
            features_active (list): list of traits from the active node.
            features_passive (list): list of traits from the passive node."""
        if 0 < s < 1:
            if random.random() < s:
                i = get_different_trait_index(features_active, features_passive)
                features_active[i] = features_passive[i]
                return True

    def __condition_centola(self, s, active, passive, neighbors):
        """Teste the conditions for similarity equal to 0.0 - in centola it is removal of the edge and attach a random node.
        
        Args:
            s (float): the similarity between two nodes.
            active (networkx.classes.nodes): the identifier for the active node.
            passive (networkx.classes.nodes): the identifier for the passive node.
            neighbors (list): list of neighbors from the active node"""
        if s == 0.0:
            self.G.remove_edge(active, passive)
            new_neighbor = get_new_neighbor(self._all_nodes, set(neighbors))
            self.G.add_edge(active, new_neighbor)
            return True


class MultilayerAxelrod(ExpandableAlgorithm):
    """The algorithm for a multilayer Axelrod.
    
    Args:
        G (networkx.classes.graph): the graph.
        population (list of list): the features and traits of the population."""
    def __init__(self, G, population):
        super(MultilayerAxelrod, self).__init__(G, population, True, False)


class MultilayerCentola(ExpandableAlgorithm):
    """The algorithm for a multilayer Centola.
    
    Args:
        G (networkx.classes.graph): the graph.
        population (list of list): the features and traits of the population."""
    def __init__(self, G, population):
        super(MultilayerCentola, self).__init__(G, population, True, True)
