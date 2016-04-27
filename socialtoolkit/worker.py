#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The source has the worker for the socialtoolkit.
"""

from __future__ import print_function

from .algorithm import Convergence
from .algorithm.evolution.axelrod import Axelrod
from .graph import normal_distribution
from .social_experiment import Experiment, EqualMultilayerExperiment

from .algorithm.analysis.graph_util import fast_get_connected_components_len, fast_get_connected_components
from .algorithm.analysis.util import get_cultural_groups, get_cultural_groups_layer, overlap_similarity_layer

import networkx as nx
from time import time
import sys

def work(parameters):
    """Returns the simulation for a given parameter dictionary.
    
    Args:
        parameters (dict): with integers width, height, features, traits, max_iterations, step_check and layers."""
    start = time()
    width = parameters['width']
    height = parameters['height']
    features = parameters['features']
    traits = parameters['traits']
    
    global_parameters = parameters['global_parameters']
    
    max_iterations = global_parameters['max_iterations']
    step_check = global_parameters['step_check']
    layers = global_parameters['layers']
    
    convergence = Convergence(max_iterations, step_check)
    population = (normal_distribution, [width*height, features, traits])
    evolution_algorithm = global_parameters['algorithm']
    
    if layers > 1:
        all_G = []
        for i in range(layers):
            all_G.append((nx.grid_2d_graph, [width, height]))
        experiment = EqualMultilayerExperiment(all_G, population, evolution_algorithm, convergence, layers)
        for i in range(0, layers):
            experiment.all_model[i].overlap_function(overlap_similarity_layer, [i, layers])
    else:
        G = (nx.grid_2d_graph, [width, height])
        experiment = Experiment(G, population, evolution_algorithm, convergence)
        
    convergence_its = experiment.converge()
    layers_output = " "
    if layers > 1:
        experiment._G = nx.compose_all(experiment.all_G)
        for i in range(0, layers):
            if i == 0:
                layers_output = ""
            if i > 0:
                layers_output += " "
            layers_output += str(fast_get_connected_components_len(experiment.all_G[i])) + " " + str(fast_get_connected_components(experiment.all_G[i])[0]) + " " + str(get_cultural_groups_layer(experiment._population, i, layers))
    else:
        layers_output = ""
    end = time()
    #print(evolution_algorithm.__name__, width, height, layers, features, traits, max_iterations, step_check, fast_get_connected_components_len(experiment._G), get_cultural_groups(experiment._population), convergence_its, (end-start), file=sys.stderr)
    return (evolution_algorithm.__name__, width, height, layers, features, traits, max_iterations, step_check, fast_get_connected_components(experiment._G)[0], fast_get_connected_components_len(experiment._G), get_cultural_groups(experiment._population), layers_output, convergence_its, (end-start))

if __name__ == "__main__":
    parameters = {}
    parameters['width'] = 5
    parameters['height'] = 5
    parameters['features'] = 5
    parameters['traits'] = 5
    
    global_parameters = {}
    global_parameters['max_iterations'] = 100000
    global_parameters['step_check'] = 10000
    global_parameters['layers'] = 1
    global_parameters['algorithm'] = Axelrod
    print(work(parameters))
