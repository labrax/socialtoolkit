#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This source is an example for a run case with multilayer.
"""

import networkx as nx

from socialtoolkit.social_experiment import EqualMultilayerExperiment
from socialtoolkit.graph import normal_distribution

from socialtoolkit.algorithm import Convergence
from socialtoolkit.algorithm.evolution import MultilayerCentola
from socialtoolkit.algorithm.analysis import CommandAnalysis, AmountIterationLayerAnalysis, OutputAnalysis

from socialtoolkit.algorithm.analysis.graph_util import fast_get_connected_components_len, fast_get_connected_components_len
from socialtoolkit.algorithm.analysis.util import get_cultural_groups_layer, get_cultural_groups, overlap_similarity_layer

from time import clock

if __name__ == "__main__":
    width = 32
    height = 32
    features = 6
    traits = 10000
    layers = 3
    max_iterations = 5*10**6
    step_check = 3*10**4
    step_analysis = 10**3
    
    all_G = []
    for i in range(layers):
        all_G.append((nx.grid_2d_graph, [width, height]))
    convergence = Convergence(max_iterations, step_check)
    evolution_algorithm = MultilayerCentola
    population = (normal_distribution, [width*height, features, traits])
    experiment = EqualMultilayerExperiment(all_G, population, evolution_algorithm, convergence, layers)
    
    analysis = [
        CommandAnalysis(0, step_analysis, fast_get_connected_components_len, [experiment.all_G[0]]),
        CommandAnalysis(0, step_analysis, fast_get_connected_components_len, [experiment.all_G[1]]),
        CommandAnalysis(0, step_analysis, fast_get_connected_components_len, [experiment.all_G[2]]),
        CommandAnalysis(0, step_analysis, get_cultural_groups_layer, [experiment._population, 0, layers]),
        CommandAnalysis(0, step_analysis, get_cultural_groups_layer, [experiment._population, 1, layers]),
        CommandAnalysis(0, step_analysis, get_cultural_groups_layer, [experiment._population, 2, layers]),
        CommandAnalysis(0, step_analysis, get_cultural_groups, [experiment._population]),
        AmountIterationLayerAnalysis(experiment._curr, layers)]
    experiment.add_analysis(analysis)
    for i in range(0, layers):
        experiment.all_model[i].overlap_function(overlap_similarity_layer, [i, layers])
    
    start = clock()
    val = experiment.converge()
    end = clock()
    
    #print end-start, val
    #print "final", get_grid_groups(experiment._G, experiment._population)
    #print "final", get_cultural_groups(experiment._population)
    #print "get_grid_groups[0]:", analysis[0].get_results()
    #print "get_grid_groups[1]:", analysis[1].get_results()
    #print "get_grid_groups[2]:", analysis[2].get_results()
    #print "get_cultural_groups:", analysis[3].get_results()
    #print "iterations for each layer:", analysis[-1].get_results()
    
    oa = OutputAnalysis(analysis[0:7], headers=["iteration", analysis[0]._function, analysis[1]._function, analysis[2]._function, analysis[3]._function, analysis[4]._function, analysis[5]._function, analysis[6]._function], output='all_info.csv')
    oa.write()
    
    """
    ob = OutputAnalysis(analysis[-2], headers=["iteration", "cultural groups"], delimeter='\t', output='cultural_groups.txt')
    ob.write()
    """
    
    oc = OutputAnalysis(analysis[-1], headers=["iteration1", "iteration2", "iteration3"], delimeter=' ')
    oc.write()
    
    """
    od = OutputAnalysis([(1, 2), (3, 4)], headers="a bunch of cool numbers", delimeter=' --> ')
    od.write()
    """
    
    oe = OutputAnalysis([end - start], headers="execution time")
    oe.write()
    
    of = OutputAnalysis([val], headers="total iterations")
    of.write()

    """
    og = OutputAnalysis([1, 2, 3, 4, 5], headers="lines?")
    og.write()
    """
