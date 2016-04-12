#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

import numpy as np

def normal_distribution(nodes, features, traits):
    population = np.zeros((nodes, features))
    for j in range(nodes):
        for i in range(features):
            population[j, i] = np.random.randint(traits)
    return population
