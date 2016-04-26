#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The source has the initializer for running the socialtoolkit.
"""

from __future__ import print_function

import sys

from socialtoolkit.graph import normal_distribution

from socialtoolkit.algorithm import Convergence
from socialtoolkit.algorithm.evolution import Axelrod, Centola, MultilayerAxelrod, MultilayerCentola

from socialtoolkit.algorithm.analysis.graph_util import fast_get_connected_components_len, fast_get_connected_components
from socialtoolkit.algorithm.analysis.util import get_cultural_groups, get_cultural_groups_layer, overlap_similarity_layer

from socialtoolkit.social_experiment import Experiment, EqualMultilayerExperiment

from socialtoolkit.errors import ParameterError

from time import time

import networkx as nx

import argparse

from multiprocessing import Pool, cpu_count

def process_args():
    """Return the processed arguments."""
    parser = argparse.ArgumentParser(
        description='Execute a simulation for a generated network and properties using a social algorithm. The ranges can be written as values to iterate in between (2 or 3 arguments) or as a list of elements.')
    parser.add_argument('-gs', '--gridsize', metavar='N', default=32, type=int, nargs='+',
        help='a range for the gridsize')
    parser.add_argument('-t', '--traits', metavar='N', default=3, type=int, nargs='+',
        help='a range for the traits')
    parser.add_argument('-f', '--features', metavar='N', default=5, type=int, nargs='+',
        help='a range for the features')
    parser.add_argument('-l', '--layers', metavar='N', default=1, type=int, nargs=1,
        help='a number of layers')
    parser.add_argument('-A', '--algorithm', metavar='<algorithm>', default="axelrod", type=str, nargs=1,
        help='an simulation algorithm, "axelrod" or "centola"')
    
    #convergence settings
    parser.add_argument('-cI', '--convergence-max-iterations', metavar='N', default=0, type=int, nargs=1,
        help='maximum number of iterations')
    parser.add_argument('-cS', '--convergence-step-check', metavar='N', default=10**4, type=int, nargs=1,
        help='step for convergence check')
    
    #multithreading
    parser.add_argument('--spark', metavar='SPARK', const="spark://10.1.1.28:7077", type=str, nargs='?',
        help='connect using spark')
    parser.add_argument('--threads', metavar='THREADS', default=cpu_count(), type=int, nargs=1,
        help='set the number of threads - default on this machine ' + str(cpu_count()))
    
    #analysis
    parser.add_argument('-p', '--physical', metavar='P', dest='physical',
        action='store_const', const=True, default=False,
        help='calculate the number of physical groups')
    parser.add_argument('-c', '--cultural', metavar='C', dest='cultural',
        action='store_const', const=True, default=False,
        help='calculate the number of cultural groups')
    parser.add_argument('-Bp', '--biggest-physical', metavar='BP', dest='biggest_physical',
        action='store_const', const=False, default=True,
        help='calculate the size of biggest physical groups')
    parser.add_argument('-Bc', '--biggest-cultural', metavar='BC', dest='biggest_cultural',
        action='store_const', const=False, default=True,
        help='calculate the size of biggest cultural groups')
    parser.add_argument('-DA', '--dont-analyse-layer-by-layer', metavar='DA', dest='no_layer_by_layer',
        action='store_const', const=True, default=False,
        help='don\'t calculate the analysis for individual layers - if on multilayer')
    parser.add_argument('-SA', '--analysis-step', metavar='N', const=sys.maxsize, type=int, nargs=1,
        help='an interval for the analysis')
    
    """
    parser.add_argument('-aO', '--analysis-output', metavar='<output file>', type=str, nargs='+',
        help='the output for analysis')

    parser.add_argument('-aA', '--analysisalgorithm', metavar='<algorithm name>', type=str, nargs='+',
        help='the algorithms for analysis')
    """
    args = parser.parse_args()
    return args

def process_range(val):
    """Returns a list for given program arguments.
    
    Args:
        val (list or int): the input parameters as specified from argparse."""
    if type(val) is not list:
        return [val]
    if len(val) == 2:
        return range(val[0], val[1]+1)
    elif len(val) == 3:
        return range(val[0], val[1]+1, val[2])
    return val

def algorithm_name_for_algorithm(val):
    """Returns the algorithm function for the program argument.
    
    Args:
        val (str or list): the name of the class."""
    if type(val) == list:
        val = val[0]
    val = val.lower()
    if val == 'axelrod':
        return Axelrod
    elif val == 'centola':
        return Centola
    else:
        print("Invalid name for algorithm '" + val + "'.", file=sys.stderr)
        exit(-1)

#@profile
def work(parameters):
    """Returns the simulation for a given parameter dictionary.
    
    Args:
        parameters (dict): with integers width, height, features, traits, max_iterations, step_check and layers."""
    start = time()
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
        if args.algorithm == Centola:
            evolution_algorithm = MultilayerCentola
        else:
            evolution_algorithm = MultilayerAxelrod
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
    args = process_args()

    #process the ranges
    args.gridsize = process_range(args.gridsize)
    args.traits = process_range(args.traits)
    args.features = process_range(args.features)
    
    #returns the algorithm class given the name
    args.algorithm = algorithm_name_for_algorithm(args.algorithm)
    
    #fix for int values
    if type(args.convergence_max_iterations) == list:
        args.convergence_max_iterations = args.convergence_max_iterations[0]
    if type(args.convergence_step_check) == list:
        args.convergence_step_check = args.convergence_step_check[0]
    if type(args.layers) == list:
        args.layers = args.layers[0]
    if type(args.threads) == list:
        args.threads = args.threads[0]
    
    #append layers fields
    layers_output = " "
    if args.layers > 1:
        for i in range(0, args.layers):
            layers_output += str(i) + "_physycal_groups " + str(i) + "_biggest_physical_group " + str(i) + "_cultural_groups "
    #print header
    print("algo width height layers features traits max_iterations step_check biggest_physical_group physical_groups cultural_groups" + layers_output + "convergence_its convergence_time")
    
    #stores all the parameters for execution
    all_P = []
    
    #generate all the parameters
    for gs in args.gridsize:
        for t in args.traits:
            for f in args.features:
                if f%args.layers != 0:
                    raise ParameterError("Invalid relation of features and layers.", "Features must be divisible by layers!", {'features' : f, 'layers' : args.layers})

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
    
    #run case for spark
    if args.spark:
        from pyspark import SparkContext, SparkConf
        conf = SparkConf().setAppName("social_simulations_" + str(time())).setMaster(args.spark)
        sc = SparkContext(conf=conf)
        sc.addPyFile("util/socialtoolkit.zip")
        ratios_RDD = sc.parallelize(all_P, len(all_P))
        prepared_work = ratios_RDD.map(work)
        result = prepared_work.collect()
        
        for i in result:
            if i == None:
                print("invalid value", file=sys.stderr)
            else:
                output = ""
                for e in i:
                    if e == "" or e == None:
                        continue
                    output += str(e) + " "
                print(output)
    else:
        if len(all_P) < args.threads:
            amount_process = len(all_P)
        else:
            amount_process = args.threads

        if amount_process > 1: #run with multiple processes
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
                        if e == "" or e == None:
                            continue
                        output += str(e) + " "
                    print(output)
        else: #run in a single process
            for x in all_P:
                result = work(x)
                output = ""
                for e in result:
                    if e == "" or e == None:
                        continue
                    output += str(e) + " "
                print(output)
