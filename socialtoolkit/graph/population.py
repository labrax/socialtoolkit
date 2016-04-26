#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This source contains methods for generating different types of population.
"""

import numpy as np

def normal_distribution(nodes, features, traits):
    """Returns a random generated population (list of list) using the random function from numpy.
    
    Args:
        nodes (int): the amount of nodes.
        features (int): the amount of features.
        traits (int): the amount of traits to choose."""
    population = np.zeros((nodes, features))
    for j in range(nodes):
        for i in range(features):
            population[j, i] = np.random.randint(traits)
    return population
