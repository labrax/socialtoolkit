#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This source contains information about a graph.
"""

class Graph(object):
    """Graph information class."""
    def __init__(self, graph_data, population_data):
        """Initiates a network with a graph and it's information of population.
        
        Args:
            graph_data (networkx.classes.graph): the graph.
            population_data (list of list): information of features and traits."""
        self.graph = graph_data
        self.population_data = population_data
