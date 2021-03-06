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

from socialtoolkit.algorithm.analysis.physical_groups import get_amount_physical_groups, get_size_biggest_physical_groups
from socialtoolkit.algorithm.analysis.cultural_groups import get_amount_cultural_groups_layer, get_amount_cultural_groups
from socialtoolkit.algorithm.analysis.util import overlap_similarity_layer

from socialtoolkit.graph.network import Network

from time import clock


def run():
    width = 5
    height = 5
    features = 6
    traits = 2
    layers = 3
    max_iterations = 3 * 10 ** 6
    step_check = 3 * 10 ** 4
    step_analysis = 10 ** 3

    all_G = []
    for i in range(layers):
        all_G.append(nx.grid_2d_graph(width, height))
    population = normal_distribution(width * height, features, traits)
    convergence = Convergence(max_iterations, step_check)
    evolution_algorithm = MultilayerCentola
    experiment = EqualMultilayerExperiment(Network(all_G, population, layers), evolution_algorithm, convergence, layers)

    analysis = [
        CommandAnalysis(0, step_analysis, get_amount_physical_groups, [experiment.network, 0]),
        CommandAnalysis(0, step_analysis, get_amount_physical_groups, [experiment.network, 1]),
        CommandAnalysis(0, step_analysis, get_amount_physical_groups, [experiment.network, 2]),
        CommandAnalysis(0, step_analysis, get_amount_cultural_groups_layer, [experiment.network, 0]),
        CommandAnalysis(0, step_analysis, get_amount_cultural_groups_layer, [experiment.network, 1]),
        CommandAnalysis(0, step_analysis, get_amount_cultural_groups_layer, [experiment.network, 2]),
        CommandAnalysis(0, step_analysis, get_amount_cultural_groups, [experiment.network]),
        AmountIterationLayerAnalysis(experiment._curr, layers)]
    experiment.add_analysis(analysis)
    for i in range(0, layers):
        experiment.all_model[i].overlap_function(overlap_similarity_layer, [i, layers])

    start = clock()
    val = experiment.converge()
    end = clock()

    # print end-start, val
    # print "final", get_grid_groups(experiment._G, experiment._population)
    # print "final", get_cultural_groups(experiment._population)
    # print "get_grid_groups[0]:", analysis[0].get_results()
    # print "get_grid_groups[1]:", analysis[1].get_results()
    # print "get_grid_groups[2]:", analysis[2].get_results()
    # print "get_cultural_groups:", analysis[3].get_results()
    # print "iterations for each layer:", analysis[-1].get_results()

    oa = OutputAnalysis(analysis[0:7],
                        headers=["iteration", analysis[0]._function, analysis[1]._function, analysis[2]._function,
                                 analysis[3]._function, analysis[4]._function, analysis[5]._function,
                                 analysis[6]._function])
    # oa.write()

    """
    ob = OutputAnalysis(analysis[-2], headers=["iteration", "cultural groups"], delimeter='\t', output='cultural_groups.txt')
    ob.write()
    """

    oc = OutputAnalysis(analysis[-1], headers=["iteration1", "iteration2", "iteration3"], delimeter=' ')
    # oc.write()

    """
    od = OutputAnalysis([(1, 2), (3, 4)], headers="a bunch of cool numbers", delimeter=' --> ')
    od.write()
    """

    oe = OutputAnalysis([end - start], headers="execution time")
    # oe.write()

    of = OutputAnalysis([val], headers="total iterations")
    # of.write()

    """
    og = OutputAnalysis([1, 2, 3, 4, 5], headers="lines?")
    og.write()
    """


if __name__ == "__main__":
    run()
