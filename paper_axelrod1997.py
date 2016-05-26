#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This source contains an example for a similar run as in Axelrod's paper.
"""

from __future__ import print_function

import networkx as nx

from socialtoolkit.social_experiment import Experiment
from socialtoolkit.graph import normal_distribution

from socialtoolkit.algorithm import Convergence
from socialtoolkit.algorithm.evolution import Axelrod, Centola, MultilayerCentola
from socialtoolkit.algorithm.analysis import CommandAnalysis

from socialtoolkit.algorithm.analysis.physical_groups import get_grid_groups_axelrod
from socialtoolkit.algorithm.analysis.cultural_groups import get_amount_cultural_groups

from socialtoolkit.graph.network import Network


def run():
    width = 10
    height = 10
    features = 3
    traits = 3
    max_iterations = 5 * 10 ** 4
    step_check = 10 ** 4
    step_analysis = 10 ** 3

    G = nx.grid_2d_graph(width, height)
    population = normal_distribution(width * height, features, traits)
    convergence = Convergence(max_iterations, step_check)
    evolution_algorithm = Axelrod
    experiment = Experiment(Network(G, population, 1), evolution_algorithm, convergence)

    analysis = [CommandAnalysis(0, step_analysis, get_grid_groups_axelrod, [experiment._G, experiment._population]),
                CommandAnalysis(0, step_analysis, get_amount_cultural_groups, [experiment._population])]
    experiment.add_analysis(analysis)

    print(experiment.converge())
    # print "final", get_grid_groups(experiment._G, experiment._population)
    # print "final", get_amount_cultural_groups(experiment._population)
    print("get_grid_groups_axelrod:", analysis[0].get_results())
    print("get_amount_cultural_groups:", analysis[1].get_results())

if __name__ == "__main__":
    run()
