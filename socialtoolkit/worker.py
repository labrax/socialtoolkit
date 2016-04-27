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

from .algorithm.analysis import CommandAnalysis, AmountIterationLayerAnalysis, OutputAnalysis
from .algorithm.analysis.graph_util import get_amount_physical_groups, get_size_biggest_physical_groups, get_amount_physical_groups_unify, get_size_biggest_physical_groups_unify
from .algorithm.analysis.util import get_amount_cultural_groups, get_size_biggest_cultural_groups, get_amount_cultural_groups_layer, get_size_biggest_cultural_groups_layer, overlap_similarity_layer

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
    evolution_algorithm = global_parameters['algorithm']
    
    analysis_step = global_parameters['analysis_step']
    no_layer_by_layer = global_parameters['no_layer_by_layer']
    physical = global_parameters['physical']
    cultural = global_parameters['cultural']
    biggest_physical = global_parameters['biggest_physical']
    biggest_cultural = global_parameters['biggest_cultural']
    output_dir = global_parameters['output_dir']
    identifier = global_parameters['identifier']
    
    this_name = "output_gs{0}_f{1}_t{2}_l{3}_{4}.csv".format(width, features, traits, layers, evolution_algorithm.__name__)
    analysis = []
    headers = ['iteration']
    
    convergence = Convergence(max_iterations, step_check)
    population = (normal_distribution, [width*height, features, traits])
    
    results = [evolution_algorithm.__name__, width, height, layers, features, traits, max_iterations, step_check]
    
    if layers > 1:
        all_G = []
        for i in range(layers):
            all_G.append((nx.grid_2d_graph, [width, height]))
        experiment = EqualMultilayerExperiment(all_G, population, evolution_algorithm, convergence, layers)
        for i in range(0, layers):
            experiment.all_model[i].overlap_function(overlap_similarity_layer, [i, layers])
        if analysis_step > 0:
            if physical:
                analysis.append(CommandAnalysis(0, analysis_step, get_amount_physical_groups_unify, [experiment.all_G]))
                headers.append('amount_physical_groups')
            if biggest_physical:
                analysis.append(CommandAnalysis(0, analysis_step, get_size_biggest_physical_groups_unify, [experiment.all_G]))
                headers.append('biggest_physical_groups')
            if cultural:
                analysis.append(CommandAnalysis(0, analysis_step, get_amount_cultural_groups, [experiment._population]))
                headers.append('amount_cultural_groups')
            if biggest_cultural:
                analysis.append(CommandAnalysis(0, analysis_step, get_size_biggest_cultural_groups, [experiment._population]))
                headers.append('biggest_cultural_groups')
            if not no_layer_by_layer:
                for i in range(0, layers):
                    if physical:
                        analysis.append(CommandAnalysis(0, analysis_step, get_amount_physical_groups, [experiment.all_G[i]]))
                        headers.append(str(i) + 'amount_physical_groups')
                    if biggest_physical:
                        analysis.append(CommandAnalysis(0, analysis_step, get_size_biggest_physical_groups, [experiment.all_G[i]]))
                        headers.append(str(i) + 'biggest_physical_groups')
                    if cultural:
                        analysis.append(CommandAnalysis(0, analysis_step, get_amount_cultural_groups_layer, [experiment._population, i, layers]))
                        headers.append(str(i) + 'amount_cultural_groups')
                    if biggest_cultural:
                        analysis.append(CommandAnalysis(0, analysis_step, get_size_biggest_cultural_groups_layer, [experiment._population, i, layers]))
                        headers.append(str(i) + 'biggest_cultural_groups')
                #analysis.append(AmountIterationLayerAnalysis(experiment._curr, layers))##to enable fix OutputAnalysis to not use, and return on results
            experiment.add_analysis(analysis)
    else:
        G = (nx.grid_2d_graph, [width, height])
        experiment = Experiment(G, population, evolution_algorithm, convergence)
        if analysis_step > 0:
            if physical:
                analysis.append(CommandAnalysis(0, analysis_step, get_amount_physical_groups, [experiment._G]))
                headers.append('amount_physical_groups')
            if biggest_physical:
                analysis.append(CommandAnalysis(0, analysis_step, get_size_biggest_physical_groups, [experiment._G]))
                headers.append('biggest_physical_groups')
            if cultural:
                analysis.append(CommandAnalysis(0, analysis_step, get_amount_cultural_groups, [experiment._population]))
                headers.append('amount_cultural_groups')
            if biggest_cultural:
                analysis.append(CommandAnalysis(0, analysis_step, get_size_biggest_cultural_groups, [experiment._population]))
                headers.append('biggest_cultural_groups')
            experiment.add_analysis(analysis)

    convergence_its = experiment.converge()
    end = time()
    results += [convergence_its, (end-start)]
    
    if analysis_step > 0:
        oa = OutputAnalysis(analysis, headers, output=output_dir+this_name)
        oa.write()
    
    if layers > 1:
        if physical:
            results.append(get_amount_physical_groups_unify(experiment.all_G))
        if biggest_physical:
            results.append(get_size_biggest_physical_groups_unify(experiment.all_G))
        if cultural:
            results.append(get_amount_cultural_groups(experiment._population))
        if biggest_cultural:
            results.append(get_size_biggest_cultural_groups(experiment._population))
        if not no_layer_by_layer:
            for i in range(0, layers):
                if physical:
                    results.append(get_amount_physical_groups(experiment.all_G[i]))
                if biggest_physical:
                    results.append(get_size_biggest_physical_groups(experiment.all_G[i]))
                if cultural:
                    results.append(get_amount_cultural_groups_layer(experiment._population, i, layers))
                if biggest_cultural:
                    results.append(get_size_biggest_cultural_groups_layer(experiment._population, i, layers))
    else:
        if physical:
            results.append(get_amount_physical_groups(experiment._G))
        if biggest_physical:
            results.append(get_size_biggest_physical_groups(experiment._G))
        if cultural:
            results.append(get_amount_cultural_groups(experiment._population))
        if biggest_cultural:
            results.append(get_size_biggest_cultural_groups(experiment._population))
    return results

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
