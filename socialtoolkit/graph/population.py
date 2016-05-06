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

def population_from_file(file_name):
    """Returns a loaded population (list of list) from a file information.
    
    Args:
        file_name (str): the file for input."""
    f = open(file_name, "r")
    header = False
    for line in f:
        if line[0] == '#':
            continue
        if header == False:
            data = line.split(" ")
            nodes = int(data[0])
            features = int(data[1])
            population = np.zeros((nodes, features))
            header = True
        else:
            data = line.split(",")
            node = data[0]
            for i in range(features):
                population[node, i] = data[i+1]
    return population
