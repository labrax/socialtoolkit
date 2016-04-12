#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function

from socialtoolkit.graph import normal_distribution

from socialtoolkit.algorithm import Convergence
from socialtoolkit.algorithm.evolution import Axelrod
from socialtoolkit.algorithm.evolution import Centola

from socialtoolkit.algorithm.analysis.graph_util import fast_get_connected_components_len
from socialtoolkit.algorithm.analysis.util import get_cultural_groups

from socialtoolkit.social_experiment import Experiment

import networkx as nx

import argparse
import sys

def process_args():
    parser = argparse.ArgumentParser(
        description='Execute a simulation for a generated network and properties using a social algorithm. The ranges can be written as values to iterate in between (2 or 3 arguments) or as a list of elements.')
    parser.add_argument('-gs', '--gridsize', metavar='N', default=32, type=int, nargs='+',
        help='a range for the gridsize')
    parser.add_argument('-t', '--traits', metavar='N', default=3, type=int, nargs='+',
        help='a range for the traits')
    parser.add_argument('-f', '--features', metavar='N', default=5, type=int, nargs='+',
        help='a range for the features')
    parser.add_argument('-cI', '--convergence-max-iterations', metavar='N', default=5*10**5, type=int, nargs=1,
        help='maximum number of iterations')
    parser.add_argument('-cS', '--convergence-step-check', metavar='N', default=10**4, type=int, nargs=1,
        help='step for convergence check')
    parser.add_argument('-A', '--algorithm', metavar='<algorithm>', default="axelrod", type=str, nargs=1,
        help='an simulation algorithm, "axelrod" or "centola"')
    """
    parser.add_argument('-p', '--physical', metavar='p', dest='calculate_physical',
        action='store_const', const=True, default=False,
        help='calculate the number of physical groups')
    parser.add_argument('-c', '--cultural', metavar='c', dest='calculate_cultural',
        action='store_const', const=True, default=False,
        help='calculate the number of cultural groups')
    parser.add_argument('-aR', '--analysisrange', metavar='N', type=int, nargs='+',
                    help='a range for the analysis')
    parser.add_argument('-aA', '--analysisalgorithm', metavar='<algorithm name>', type=str, nargs='+',
                    help='the algorithms for analysis')
    parser.add_argument('-aO', '--analysisoutput', metavar='<output file>', type=str, nargs='+',
                    help='the output for analysis')
    """
    args = parser.parse_args()
    return args

def process_range(val):
    if type(val) is not list:
        return [val]
    if len(val) == 2:
        return range(val[0], val[1])
    elif len(val) == 3:
        return range(val[0], val[1], val[2])
    return val

def algorithm_name_for_algorithm(val):
    if val == 'axelrod':
        return Axelrod
    elif val == 'centola':
        return Centola
    else:
        print("Invalid name for algorithm '" + val + "'.", file=sys.stderr)
        exit(-1)

if __name__ == "__main__":
    args = process_args()

    print(args)
    
    args.algorithm = algorithm_name_for_algorithm(args.algorithm)
    
    print("width, height, features, traits, max_iterations, step_check, fast_get_connected_components_len(experiment._G), get_cultural_groups(experiment._population), convergence_its")
    
    args.gridsize = process_range(args.gridsize)
    for gs in args.gridsize:
        args.traits = process_range(args.traits)
        for t in args.traits:
            args.features = process_range(args.features)
            for f in args.features:
                width = gs
                height = gs
                features = f
                traits = t
                max_iterations = args.convergence_max_iterations
                step_check = args.convergence_step_check
                
                G = (nx.grid_2d_graph, [width, height])
                convergence = Convergence(max_iterations, step_check)
                evolution_algorithm = args.algorithm
                population = (normal_distribution, [width*height, features, traits])
                experiment = Experiment(G, population, evolution_algorithm, convergence)
                
                convergence_its = experiment.converge()
                print(width, height, features, traits, max_iterations, step_check, fast_get_connected_components_len(experiment._G), get_cultural_groups(experiment._population), convergence_its)
    
