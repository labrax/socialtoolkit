#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This source contains information about a graph.
"""

import networkx as nx

class Graph(object):
    """Graph information class."""
    def __init__(self, graph_data, population_data):
        """Initiates a network with a graph and it's information of population.
        
        Args:
            graph_data (networkx.classes.graph): the graph.
            population_data (list of list): information of features and traits."""
        self.graph = graph_data
        self.population_data = population_data

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
        if header == False:
            nodes = int(line.split(" ")[0])
            for i in range(0, nodes):
                G.add_node(int(i))
            header = True
        else:
            data = line.split(",")
            G.add_edge(int(data[0]), int(data[1]))
    return G
