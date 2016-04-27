#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The source has the initializer for running the socialtoolkit.
"""

from __future__ import print_function

from socialtoolkit.algorithm.evolution import Axelrod, Centola, MultilayerAxelrod, MultilayerCentola
from socialtoolkit.errors import ParameterError
from socialtoolkit.worker import work

import argparse
import sys
from multiprocessing import Pool, cpu_count
from time import time

class STK:
    def __init__(self):
        self.args = self.__process_args()

        #process the ranges
        self.args.gridsize = self.__process_range(self.args.gridsize)
        self.args.traits = self.__process_range(self.args.traits)
        self.args.features = self.__process_range(self.args.features)
        
        #fix for int values
        if type(self.args.convergence_max_iterations) == list:
            self.args.convergence_max_iterations = self.args.convergence_max_iterations[0]
        if type(self.args.convergence_step_check) == list:
            self.args.convergence_step_check = self.args.convergence_step_check[0]
        if type(self.args.layers) == list:
            self.args.layers = self.args.layers[0]
        if type(self.args.threads) == list:
            self.args.threads = self.args.threads[0]
        if type(self.args.analysis_step) == list:
            self.args.analysis_step = self.args.analysis_step[0]
        if type(self.args.output_dir) == list:
            self.args.output_dir = self.args.output_dir[0]
            
        #returns the algorithm class given the name
        self.args.algorithm = self.__algorithm_name_for_algorithm(self.args.algorithm, self.args.layers)
        self.all_P = self.__exec_params(self.args) #store all the parameters for execution
    def run(self):
        result = []
        #run case for spark
        if self.args.spark:
            from pyspark import SparkContext, SparkConf
            conf = SparkConf().setAppName("social_simulations_" + str(time())).setMaster(args.spark) ###TODO: change?
            sc = SparkContext(conf=conf)
            sc.addPyFile("util/socialtoolkit.zip")
            ratios_RDD = sc.parallelize(all_P, len(all_P))
            prepared_work = ratios_RDD.map(work)
            result = prepared_work.collect()
        else:
            if len(self.all_P) < self.args.threads:
                amount_process = len(self.all_P)
            else:
                amount_process = self.args.threads

            if amount_process > 1: #run with multiple processes
                pool = Pool(processes=amount_process)
                result = pool.map(work, self.all_P)
                pool.close()
                pool.join()
            else: #run in a single process
                for i in self.all_P:
                    result.append(work(i))
        return result
    def write(self, result, file=sys.stdout):
        for i in result:
            if i == None:
                print("invalid value", file=sys.stderr)
            else:
                output = ""
                for e in i:
                    if e == "" or e == None:
                        continue
                    output += str(e) + " "
                print(output, file=file)
    def __exec_params(self, args):
        """Returns the list of parameters for execution.
        
        Args:
            args (Namespace): the processed arguments of the program."""
        all_P = []
        
        global_parameters = {}
        global_parameters['algorithm'] = args.algorithm
        global_parameters['max_iterations'] = args.convergence_max_iterations
        if global_parameters['max_iterations'] == 0:
            global_parameters['max_iterations'] = 150000*10*args.traits[-1]
        global_parameters['step_check'] = args.convergence_step_check
        global_parameters['layers'] = args.layers

        if args.physical or args.cultural or args.biggest_physical or args.biggest_cultural:
            global_parameters['physical'] = args.physical
            global_parameters['cultural'] = args.cultural
            global_parameters['biggest_physical'] = args.biggest_physical
            global_parameters['biggest_cultural'] = args.biggest_cultural
        else:
            global_parameters['physical'] = True
            global_parameters['cultural'] = True
            global_parameters['biggest_physical'] = True
            global_parameters['biggest_cultural'] = True
        global_parameters['no_layer_by_layer'] = args.no_layer_by_layer
        global_parameters['analysis_step'] = args.analysis_step
        global_parameters['output_dir'] = args.output_dir
        global_parameters['id'] = str(time())
        
        #generate all the parameters
        for gs in args.gridsize:
            for t in args.traits:
                for f in args.features:
                    if f%args.layers != 0:
                        #raise ParameterError("Invalid relation of features and layers.", "Features must be divisible by layers!", {'features' : f, 'layers' : args.layers})
                        print("Invalid relation of features and layers.\nFeatures must be divisible by layers! Skipping features and layers: ", features, layers)
                        continue

                    parameters = {}
                    parameters['width'] = gs
                    parameters['height'] = gs
                    parameters['features'] = f
                    parameters['traits'] = t
                    
                    parameters['global_parameters'] = global_parameters
                    all_P.append(parameters)
        
        return all_P
    def __process_args(self): #return args from sys.argv
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
        parser.add_argument('--threads', metavar='THREADS', dest='threads', default=cpu_count(), type=int, nargs=1,
            help='set the number of threads - default on this machine ' + str(cpu_count()))
        
        #analysis
        parser.add_argument('-p', '--physical', metavar='P', dest='physical',
            action='store_const', const=True, default=False,
            help='calculate the number of physical groups')
        parser.add_argument('-c', '--cultural', metavar='C', dest='cultural',
            action='store_const', const=True, default=False,
            help='calculate the number of cultural groups')
        parser.add_argument('-Bp', '--biggest-physical', metavar='BP', dest='biggest_physical',
            action='store_const', const=True, default=False,
            help='calculate the size of biggest physical groups')
        parser.add_argument('-Bc', '--biggest-cultural', metavar='BC', dest='biggest_cultural',
            action='store_const', const=True, default=False,
            help='calculate the size of biggest cultural groups')
        parser.add_argument('-DA', '--dont-analyse-layer-by-layer', metavar='DA', dest='no_layer_by_layer',
            action='store_const', const=True, default=False,
            help='don\'t calculate the analysis for individual layers - if on multilayer')
        parser.add_argument('-SA', '--analysis-step', metavar='N', dest='analysis_step', default=sys.maxsize, type=int, nargs=1,
            help='an interval for the analysis')
        parser.add_argument('-OA', '--analysis-output', metavar='OUTPUT-DIR', dest='output_dir', default="/userdata/vroth/output_data/", type=str, nargs=1,
            help='a folder for the output of analysis')
        
        """
        parser.add_argument('-aO', '--analysis-output', metavar='<output file>', type=str, nargs='+',
            help='the output for analysis')

        parser.add_argument('-aA', '--analysisalgorithm', metavar='<algorithm name>', type=str, nargs='+',
            help='the algorithms for analysis')
        """
        args = parser.parse_args()
        return args
    def __process_range(self, val): #return range from parameters
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
    def __algorithm_name_for_algorithm(self, val, layers): #return algorithm from str
        """Returns the algorithm function for the program argument.
        
        Args:
            val (str or list): the name of the class.
            layers (int): the amount of layers."""
        if type(val) == list:
            val = val[0]
        val = val.lower()
        if layers > 1:
            if val == 'axelrod':
                return MultilayerAxelrod
            elif val == 'centola':
                return MultilayerCentola
        else:
            if val == 'axelrod':
                return Axelrod
            elif val == 'centola':
                return Centola
        print("Invalid name for algorithm '" + val + "'.", file=sys.stderr)
        exit(-1)


if __name__ == "__main__":
    stk = STK()
    #append layers fields
    layers_output = " "
    if stk.args.layers > 1:
        for i in range(0, args.layers):
            layers_output += str(i) + "_physycal_groups " + str(i) + "_biggest_physical_group " + str(i) + "_cultural_groups "
    #print header
    print("algo width height layers features traits max_iterations step_check biggest_physical_group physical_groups cultural_groups" + layers_output + "convergence_its convergence_time")
    stk.write(stk.run())
