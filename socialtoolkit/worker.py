#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The source has the worker for the socialtoolkit.
"""

from __future__ import print_function

from .algorithm import Convergence
from .graph import normal_distribution, population_from_file, graph_from_file
from .social_experiment import Experiment, EqualMultilayerExperiment
from .algorithm.analysis import CommandAnalysis, AmountIterationLayerAnalysis, OutputAnalysis
from .algorithm.analysis.physical_groups import get_amount_physical_groups, get_size_biggest_physical_groups, get_amount_physical_groups_unify, get_size_biggest_physical_groups_unify
from .algorithm.analysis.cultural_groups import get_amount_cultural_groups, get_size_biggest_cultural_groups, get_amount_cultural_groups_layer, get_size_biggest_cultural_groups_layer
from .algorithm.analysis.util import overlap_similarity_layer
from .algorithm.evolution import Axelrod, Centola, Klemm, MultilayerAxelrod, MultilayerCentola, MultilayerKlemm
from .graph.network import Network, graph_to_file, population_to_file

import networkx as nx
from time import time


valid_algorithms = ['axelrod', 'centola', 'klemm']


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

    directed = global_parameters['directed_graph']

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

    population_input = global_parameters['population_input']
    graph_input = global_parameters['graph_input']

    population_output = global_parameters['population_output']
    graph_output = global_parameters['graph_output']

    if layers > 1:
        if evolution_algorithm == 'axelrod':
            evolution_algorithm = MultilayerAxelrod
        elif evolution_algorithm == 'centola':
            evolution_algorithm = MultilayerCentola
        elif evolution_algorithm == 'klemm':
            evolution_algorithm = MultilayerKlemm
    elif layers == 1:
        if evolution_algorithm == 'axelrod':
            evolution_algorithm = Axelrod
        elif evolution_algorithm == 'centola':
            evolution_algorithm = Centola
        elif evolution_algorithm == 'klemm':
            evolution_algorithm = Klemm

    this_name = "output_gs{0}_f{1}_t{2}_l{3}_{4}".format(width, features, traits, layers, evolution_algorithm.__name__)
    analysis = []
    headers = ['iteration']

    convergence = Convergence(max_iterations, step_check)

    if type(population_input) == str:
        population = population_from_file(population_input)
        width = "file:"+population_input
        height = "file"
        features = "file"
        traits = "file"
    else:
        population = normal_distribution(width*height, features, traits)

    results = parameters.copy()
    results.pop('global_parameters')

    #results = [evolution_algorithm.__name__, width, height, layers, features, traits, max_iterations, step_check]

    if layers > 1:
        all_graphs = []
        for i in range(layers):
            if type(graph_input) == str:
                all_graphs.append(graph_from_file(graph_input, directed, i, layers))
            else:
                if directed:
                    all_graphs.append(nx.grid_2d_graph(width, height).to_directed())
                else:
                    all_graphs.append(nx.grid_2d_graph(width, height))
        network = Network(all_graphs, population, layers)
        experiment = EqualMultilayerExperiment(network, evolution_algorithm, convergence, layers, **parameters)
        for i in range(0, layers):
            experiment.all_model[i].overlap_function(overlap_similarity_layer, [i, layers])
        if analysis_step > 0:
            if physical:
                analysis.append(CommandAnalysis(0, analysis_step, get_amount_physical_groups_unify, [network]))
                headers.append('amount_physical_groups')
            if biggest_physical:
                analysis.append(CommandAnalysis(0, analysis_step, get_size_biggest_physical_groups_unify, [network]))
                headers.append('biggest_physical_groups')
            if cultural:
                analysis.append(CommandAnalysis(0, analysis_step, get_amount_cultural_groups, [network]))
                headers.append('amount_cultural_groups')
            if biggest_cultural:
                analysis.append(CommandAnalysis(0, analysis_step, get_size_biggest_cultural_groups, [network]))
                headers.append('biggest_cultural_groups')
            if not no_layer_by_layer:
                for i in range(0, layers):
                    if physical:
                        analysis.append(CommandAnalysis(0, analysis_step, get_amount_physical_groups, [network, i]))
                        headers.append(str(i) + 'amount_physical_groups')
                    if biggest_physical:
                        analysis.append(CommandAnalysis(0, analysis_step, get_size_biggest_physical_groups, [network, i]))
                        headers.append(str(i) + 'biggest_physical_groups')
                    if cultural:
                        analysis.append(CommandAnalysis(0, analysis_step, get_amount_cultural_groups_layer, [network, i]))
                        headers.append(str(i) + 'amount_cultural_groups')
                    if biggest_cultural:
                        analysis.append(CommandAnalysis(0, analysis_step, get_size_biggest_cultural_groups_layer, [network, i]))
                        headers.append(str(i) + 'biggest_cultural_groups')
                        # analysis.append(AmountIterationLayerAnalysis(experiment._curr, layers))##to enable fix OutputAnalysis to not use, and return on results
            experiment.add_analysis(analysis)
    else:
        if type(graph_input) == str:
            graph = graph_from_file(graph_input, directed)
        else:
            if directed:
                graph = nx.grid_2d_graph(width, height).to_directed()
            else:
                graph = nx.grid_2d_graph(width, height)
        network = Network(graph, population, layers)
        experiment = Experiment(network, evolution_algorithm, convergence, **parameters)
        if analysis_step > 0:
            if physical:
                analysis.append(CommandAnalysis(0, analysis_step, get_amount_physical_groups, [network]))
                headers.append('amount_physical_groups')
            if biggest_physical:
                analysis.append(CommandAnalysis(0, analysis_step, get_size_biggest_physical_groups, [network]))
                headers.append('biggest_physical_groups')
            if cultural:
                analysis.append(CommandAnalysis(0, analysis_step, get_amount_cultural_groups, [network]))
                headers.append('amount_cultural_groups')
            if biggest_cultural:
                analysis.append(CommandAnalysis(0, analysis_step, get_size_biggest_cultural_groups, [network]))
                headers.append('biggest_cultural_groups')
            experiment.add_analysis(analysis)

    convergence_its = experiment.converge()
    end = time()

    results['convergence_iterations'] = convergence_its
    results['convergence_time'] = end-start

    if analysis_step > 0:
        oa = OutputAnalysis(analysis, headers, output=output_dir+this_name+".csv")
        oa.write()

    if graph_output:
        graph_to_file(network, this_name + ".el")
    if population_output:
        population_to_file(network, this_name + ".pd")

    if layers > 1:  # final results data
        if physical:
            results['amount_physical_groups'] = get_amount_physical_groups_unify(network)
        if biggest_physical:
            results['biggest_physical_group'] = get_size_biggest_physical_groups_unify(network)
        if cultural:
            results['amount_cultural_groups'] = get_amount_cultural_groups(network)
        if biggest_cultural:
            results['biggest_cultural_group'] = get_size_biggest_cultural_groups(network)
        if not no_layer_by_layer:
            for i in range(0, layers):
                if physical:
                    results['amount_physical_groups' + str(i)] = get_amount_physical_groups(network, i)
                if biggest_physical:
                    results['biggest_physical_group' + str(i)] = get_size_biggest_physical_groups(network, i)
                if cultural:
                    results['amount_cultural_groups' + str(i)] = get_amount_cultural_groups_layer(network, i)
                if biggest_cultural:
                    results['biggest_cultural_group' + str(i)] = get_size_biggest_cultural_groups_layer(network, i)
    else:
        if physical:
            results['amount_physical_groups'] = get_amount_physical_groups(network)
        if biggest_physical:
            results['biggest_physical_group'] = get_size_biggest_physical_groups(network)
        if cultural:
            results['amount_cultural_groups'] = get_amount_cultural_groups(network)
        if biggest_cultural:
            results['biggest_cultural_group'] = get_size_biggest_cultural_groups(network)
    return results
