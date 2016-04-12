#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

import networkx as nx

from socialtoolkit.social_experiment import Experiment
from socialtoolkit.graph import normal_distribution

from socialtoolkit.algorithm import Convergence
from socialtoolkit.algorithm.evolution import Axelrod
from socialtoolkit.algorithm.evolution import Centola
from socialtoolkit.algorithm.evolution import ExpandableAlgorithm
from socialtoolkit.algorithm.analysis import CommandAnalysis

from socialtoolkit.algorithm.analysis.graph_util import get_grid_groups
from socialtoolkit.algorithm.analysis.util import get_cultural_groups

if __name__ == "__main__":
    width = 10
    height = 10
    features = 3
    traits = 3
    max_iterations = 5*10**4
    step_check = 10**4
    step_analysis = 10**3
    
    G = (nx.grid_2d_graph, [width, height])
    convergence = Convergence(max_iterations, step_check)
    evolution_algorithm = Axelrod
    population = (normal_distribution, [width*height, features, traits])
    experiment = Experiment(G, population, evolution_algorithm, convergence)
    
    analysis = [CommandAnalysis(0, step_analysis, get_grid_groups, [experiment._G, experiment._population]),
        CommandAnalysis(0, step_analysis, get_cultural_groups, [experiment._population])]
    experiment.add_analysis(analysis)
    
    print experiment.converge()
    #print "final", get_grid_groups(experiment._G, experiment._population)
    #print "final", get_cultural_groups(experiment._population)
    print "get_grid_groups:", analysis[0].get_results()
    print "get_cultural_groups:", analysis[1].get_results()
    
