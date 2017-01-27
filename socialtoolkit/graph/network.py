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
    """
    Graph information class.
    """
    network_ids = 0

    @staticmethod
    def _new_id():
        Network.network_ids += 1
        return Network.network_ids

    def __init__(self, graph_data, population_data, layers, id=True):
        """
        Initiates a network with a graph and it's information of population.
        :param graph_data (networkx.classes.graph): the graph.
        :param population_data (list of list): information of features and traits.
        """
        if type(graph_data) == list:
            self.graph = graph_data
        else:
            self.graph = [graph_data]
        self.population_data = population_data
        self.layers = layers
        if id:
            self.id = Network._new_id()
        else:
            self.id = 0


def graph_from_file(file_name, directed=False, curr_layer=0, amount_layers=0):
    """Returns a loaded graph (nx.classes.graph) from an edge file.
    
    Args:
        file_name (str): the file for input.
        directed (bool): whether the graph is directed or not.
        curr_layer (Optional[int]): the current layer index.
        amount_layers (Optional[int]): the amount of layers."""
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    f = open(file_name, "r")
    header = False
    for line in f:
        if line[0] == '#':
            continue
        if not header:
            nodes = int(line.split(" ")[0])
            for i in range(0, nodes): #FIXME: Change after implementation of graph tool, see(http://stackoverflow.com/questions/36193773/graph-tool-surprisingly-slow-compared-to-networkx)
                G.add_node(int(i))
            header = True
        else:
            data = line.split(",")
            G.add_edge(int(data[0]), int(data[1]))
    f.close()
    return G


def graph_to_file(network, file_name, print_amount_nodes=True, delimeter=","):
    """

    :param network:
    :param file_name:
    :param print_amount_nodes:
    :param delimeter:
    :return:
    """
    output_f = open(file_name, 'w')

    new_network = nx.compose_all(network.graph)
    nodes = dict()
    i = 1
    for n in new_network.nodes():
        nodes[n] = i
        i += 1
    if print_amount_nodes:
        output_f.write(str(i-1) + "\n")
    for e1, e2 in new_network.edges():
        output_f.write(delimeter.join([str(nodes[e1]), str(nodes[e2])]) + "\n")
    output_f.close()


def population_to_file(network, file_name):
    """

    :param network:
    :param file_name:
    :return:
    """
    output_f = open(file_name, 'w')
    for index in range(len(network.population_data)):
        values = list()
        for v in network.population_data[index]:
            values.append(str(int(v)))
        output_f.write(str(index+1) + "," + ",".join(values) + "\n")
    output_f.close()


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
            node = int(data[0])
            for i in range(features):
                population[node, i] = data[i+1]
    f.close()
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
