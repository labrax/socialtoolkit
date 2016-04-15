#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

from __future__ import print_function

from socialtoolkit.graph import normal_distribution

from socialtoolkit.algorithm import Convergence
from socialtoolkit.algorithm.evolution import Axelrod, Centola, ExpandableCentolaAlgorithm

from socialtoolkit.algorithm.analysis.graph_util import fast_get_connected_components_len
from socialtoolkit.algorithm.analysis.util import get_cultural_groups, overlap_similarity_layer

from socialtoolkit.social_experiment import Experiment, EqualMultilayerExperiment

from multiprocessing import Pool

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
    parser.add_argument('-cI', '--convergence-max-iterations', metavar='N', default=0, type=int, nargs=1,
        help='maximum number of iterations')
    parser.add_argument('-cS', '--convergence-step-check', metavar='N', default=10**4, type=int, nargs=1,
        help='step for convergence check')
    parser.add_argument('-A', '--algorithm', metavar='<algorithm>', default="axelrod", type=str, nargs=1,
        help='an simulation algorithm, "axelrod" or "centola"')
    parser.add_argument('-l', '--layers', metavar='N', default=1, type=int, nargs=1,
        help='a number of layers')
    parser.add_argument('--spark', metavar='SPARK', dest='spark',
        action='store_const', const=True, default=False,
        help='connect using spark')
    """
    parser.add_argument('-aR', '--analysisinterval', metavar='N', type=int, nargs='+',
                    help='an interval for the analysis')
    parser.add_argument('-p', '--physical', metavar='p', dest='calculate_physical',
        action='store_const', const=True, default=False,
        help='calculate the number of physical groups')
    parser.add_argument('-c', '--cultural', metavar='c', dest='calculate_cultural',
        action='store_const', const=True, default=False,
        help='calculate the number of cultural groups')
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
        return range(val[0], val[1]+1)
    elif len(val) == 3:
        return range(val[0], val[1]+1, val[2])
    return val

def algorithm_name_for_algorithm(val):
    if type(val) == list:
        val = val[0]
    if val == 'axelrod':
        return Axelrod
    elif val == 'centola':
        return Centola
    else:
        print("Invalid name for algorithm '" + val + "'.", file=sys.stderr)
        exit(-1)

#@profile
def work(parameters):
    width = parameters['width']
    height = parameters['height']
    features = parameters['features']
    traits = parameters['traits']
    max_iterations = parameters['max_iterations']
    step_check = parameters['step_check']
    layers = parameters['layers']
    
    convergence = Convergence(max_iterations, step_check)
    population = (normal_distribution, [width*height, features, traits])
    
    if layers > 1:
        evolution_algorithm = ExpandableCentolaAlgorithm
        all_G = []
        for i in range(layers):
            all_G.append((nx.grid_2d_graph, [width, height]))
        experiment = EqualMultilayerExperiment(all_G, population, evolution_algorithm, convergence, layers)
        for i in range(0, layers):
            experiment.all_model[i].overlap_function(overlap_similarity_layer, [i, layers])
    else:
        evolution_algorithm = args.algorithm
        G = (nx.grid_2d_graph, [width, height])
        experiment = Experiment(G, population, evolution_algorithm, convergence)
        
    convergence_its = experiment.converge()
    if layers > 1:
        experiment._G = nx.compose_all(experiment.all_G)
    return (evolution_algorithm.__name__, width, height, layers, features, traits, max_iterations, step_check, fast_get_connected_components_len(experiment._G), get_cultural_groups(experiment._population), convergence_its)

if __name__ == "__main__":
    args = process_args()

    args.gridsize = process_range(args.gridsize)
    args.traits = process_range(args.traits)
    args.features = process_range(args.features)
    
    args.algorithm = algorithm_name_for_algorithm(args.algorithm)
    
    if type(args.convergence_max_iterations) == list:
        args.convergence_max_iterations = args.convergence_max_iterations[0]
    if type(args.convergence_step_check) == list:
        args.convergence_step_check = args.convergence_step_check[0]
    if type(args.layers) == list:
        args.layers = args.layers[0]
    if args.layers > 1 and args.algorithm == Axelrod:
        print("More than 1 layers must use Centola!", file=sys.stderr)
        exit(-1)
    
    print("algo width height layers features traits max_iterations step_check physical_groups cultural_groups convergence_its")
    
    all_P = []
    
    for gs in args.gridsize:
        for t in args.traits:
            for f in args.features:
                parameters = {}
                parameters['width'] = gs
                parameters['height'] = gs
                parameters['features'] = f
                parameters['traits'] = t
                parameters['max_iterations'] = args.convergence_max_iterations
                if parameters['max_iterations'] == 0:
                    parameters['max_iterations'] = 150000*10*t
                parameters['step_check'] = args.convergence_step_check
                parameters['layers'] = args.layers
                all_P.append(parameters)
    
    if args.spark == True:
        from pyspark import SparkContext, SparkConf
        from time import time
        conf = SparkConf().setAppName("social_simulations_" + str(time())).setMaster("spark://10.1.1.28:7077")
        sc = SparkContext(conf=conf)
        ratios_RDD = sc.parallelize(all_P)
        results = ratios_RDD.map(work)
        results.collect()
        
        for i in result:
            if result == None:
                print("invalid value", file=sys.stderr)
            else:
                output = ""
                for e in i:
                    output += str(e) + " "
                print(output)
    else:
        amount_process = len(all_P)
        if amount_process > 8:
            amount_process = 8

        if amount_process > 1:
            pool = Pool(processes=amount_process)
            result = pool.map(work, all_P)
            pool.close()
            pool.join()
            for i in result:
                if result == None:
                    print("invalid value", file=sys.stderr)
                else:
                    output = ""
                    for e in i:
                        output += str(e) + " "
                    print(output)
        else:
            result = work(all_P[0])
            output = ""
            for e in result:
                output += str(e) + " "
            print(output)
