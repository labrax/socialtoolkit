#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This source contains information about a a network, graph and population generation.
"""

import networkx as nx
import numpy as np
import random
import math

class Network(object):
    """Graph information class."""
    def __init__(self, graph_data, population_data, layers):
        """Initiates a network with a graph and it's information of population.
        
        Args:
            graph_data (networkx.classes.graph): the graph.
            population_data (list of list): information of features and traits."""
        self.graph = graph_data
        self.population_data = population_data
        self.layers = layers


def graph_from_file(file_name, curr_layer=0, amount_layers=0):
    """Returns a loaded graph (nx.classes.graph) from an edge file.
    
    Args:
        file_name (str): the file for input.
        curr_layer (Optional[int]): the current layer index.
        amount_layers (Optional[int]): the amount of layers."""
    G = nx.Graph()
    f = open(file_name, "r")
    header = False
    for line in f:
        if line[0] == '#':
            continue
        if not header:
            nodes = int(line.split(" ")[0])
            for i in range(0, nodes):
                G.add_node(int(i))
            header = True
        else:
            data = line.split(",")
            G.add_edge(int(data[0]), int(data[1]))
    return G


def population_from_file(file_name):
    """Returns a loaded population (list of list) from a file information.
    
    Args:
        file_name (str): the file for input."""
    f = open(file_name, "r")
    header = False
    features = None
    population = None
    for line in f:
        if line[0] == '#':
            continue
        if header is False:
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


def _get_power_law_distribution(q, gama=1+math.log(3)/math.log(2)):
    """return an array of q numbers within 0 and 1 distributed like a discrete power law"""
    distr = []
    curr_sum = 0
    for i in range(q):
        distr.append((i+1)**(-gama))
        curr_sum += ((i+1)**(-gama))
    for i in range(q):
        distr[i] = distr[i]/curr_sum
    return distr


def power_law_distribution(nodes, features, traits):
    """Returns a random generated population (list of list) using a power law-like distribution from numpy.
    
    Args:
        nodes (int): the amount of nodes.
        features (int): the amount of features.
        traits (int): the amount of traits to choose."""
    d = _get_power_law_distribution(traits)
    for i in range(1, len(d)):
        d[i] = d[i]+d[i-1]
    d[-1] = 1

    val = dict()

    population = np.zeros((nodes, features))
    for j in range(nodes):
        for i in range(features):
            v = random.random()
            for k in range(len(d)):
                if v <= d[k]:
                    val[k] = val.get(k, 0) + 1  # val indicates the amount of each trait
                    population[j, i] = k
                    break
    return population
