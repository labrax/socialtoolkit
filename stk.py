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
from multiprocessing import Pool, cpu_count
from time import time, ctime
import sys

class STK:
    def __init__(self):
        self.run_id = ctime().replace(' ', '_')
        self.args = self.__process_args()

        #process the ranges
        self.args.gridsize = self.__process_range(self.args.gridsize)
        self.args.traits = self.__process_range(self.args.traits)
        self.args.features = self.__process_range(self.args.features)

        #fix for int/str in list values
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
        if type(self.args.graph_input) == list:
            self.args.graph_input = self.args.graph_input[0]
        if type(self.args.population_input) == list:
            self.args.population_input = self.args.population_input[0]
        if self.args.output_dir[-1] != '/':
            self.args.output_dir += '/'
        if self.args.analysis_step != 0:
            self.__prepare_dir(self.args.output_dir)
            
        #returns the algorithm class given the name
        self.args.algorithm = self.__algorithm_name_for_algorithm(self.args.algorithm, self.args.layers)
        #store all the parameters for execution
        self.all_P = self.__exec_params(self.args)
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
        parser.add_argument('-SA', '--analysis-step', metavar='N', dest='analysis_step', default=0, type=int, nargs=1,
            help='an interval for the analysis')
        parser.add_argument('-OA', '--analysis-output', metavar='OUTPUT-DIR', dest='output_dir', default="/userdata/vroth/output_data/run_" + str(self.run_id), type=str, nargs=1,
            help='a folder for the output of analysis')
            
        parser.add_argument('-IP', '--input-population', metavar='POPULATION_INPUT_FILE', dest='population_input', type=str, nargs=1,
            help='an input population file')
        parser.add_argument('-IG', '--input-graph', metavar='GRAPH_INPUT_FILE', dest='graph_input', type=str, nargs=1,
            help='an input graph file')
        
        args = parser.parse_args()
        print(args.graph_input, args.population_input)
        #exit(-1)
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

        if args.physical == False and args.cultural == False and args.biggest_physical == False and args.biggest_cultural == False:
            args.physical = True
            args.cultural = True
            args.biggest_physical = True
            args.biggest_cultural = True
        global_parameters['physical'] = args.physical
        global_parameters['cultural'] = args.cultural
        global_parameters['biggest_physical'] = args.biggest_physical
        global_parameters['biggest_cultural'] = args.biggest_cultural

        global_parameters['no_layer_by_layer'] = args.no_layer_by_layer
        global_parameters['analysis_step'] = args.analysis_step
        global_parameters['output_dir'] = args.output_dir
        global_parameters['identifier'] = self.run_id
        
        global_parameters['graph_input'] = args.graph_input
        global_parameters['population_input'] = args.population_input
        
        #generate all the parameters
        for gs in args.gridsize:
            for t in args.traits:
                for f in args.features:
                    if f%args.layers != 0:
                        #raise ParameterError("Invalid relation of features and layers.", "Features must be divisible by layers!", {'features' : f, 'layers' : args.layers})
                        print("Invalid relation of features and layers.\nFeatures must be divisible by layers! Skipping features and layers: ", f, self.args.layers)
                        continue

                    parameters = {}
                    parameters['width'] = gs
                    parameters['height'] = gs
                    parameters['features'] = f
                    parameters['traits'] = t
                    
                    parameters['global_parameters'] = global_parameters
                    all_P.append(parameters)
        
        return all_P
    def __prepare_dir(self, directory):
        import re
        import os
        for i in re.finditer('/', directory):
            if directory[i.start()-1] == '/' or i.start() == 0:
                continue
            curr = directory[:i.start()]
            try:
                os.mkdir(curr)
            except OSError as e:
                if e.errno == 17:
                    pass
    def run(self):
        result = []
        #run case for spark
        if self.args.spark:
            from pyspark import SparkContext, SparkConf
            conf = SparkConf().setAppName("social_simulations_" + str(self.run_id)).setMaster(self.args.spark)
            sc = SparkContext(conf=conf)
            sc.addPyFile("util/socialtoolkit.zip")
            ratios_RDD = sc.parallelize(self.all_P, len(self.all_P))
            prepared_work = ratios_RDD.map(work)
            result = prepared_work.collect()
        else:
            if len(self.all_P) < self.args.threads:
                amount_process = len(self.all_P)
            else:
                amount_process = self.args.threads

            if amount_process > 1: #run with multiple processes
                pool = Pool(processes=amount_process)
                result = pool.imap(work, self.all_P)
                pool.close()
                pool.join()
            else: #run in a single process
                for i in self.all_P:
                    result.append(work(i))
        return result
    def get_headers(self):
        if hasattr(self, "headers"):
            return self.headers
        self.headers = ["algorithm", "width", "height", "layers", "features", "traits", "convergence_max_iterations", "convergence_step_check", "convergence_iterations", "convergence_time"]
        if self.args.layers > 1:
            if self.args.physical:
                self.headers.append("amount_physical_groups")
            if self.args.biggest_physical:
                self.headers.append("biggest_physical_groups")
            if self.args.cultural:
                self.headers.append("amount_cultural_groups")
            if self.args.biggest_cultural:
                self.headers.append("biggest_cultural_groups")
            if not self.args.no_layer_by_layer:
                for i in range(0, self.args.layers):
                    if self.args.physical:
                        self.headers.append(str(i) + "amount_physical_groups")
                    if self.args.biggest_physical:
                        self.headers.append(str(i) + "biggest_physical_groups")
                    if self.args.cultural:
                        self.headers.append(str(i) + "amount_cultural_groups")
                    if self.args.biggest_cultural:
                        self.headers.append(str(i) + "biggest_cultural_groups")
        else:
            if self.args.physical:
                self.headers.append("amount_physical_groups")
            if self.args.biggest_physical:
                self.headers.append("biggest_physical_groups")
            if self.args.cultural:
                self.headers.append("amount_cultural_groups")
            if self.args.biggest_cultural:
                self.headers.append("biggest_cultural_groups")
        return self.headers
    def write(self, result, delimeter=',', file=sys.stdout):
        print(delimeter.join(str(i) for i in self.get_headers()), file=file)
        for i in result:
            if i == None:
                print("invalid value", file=sys.stderr)
            else:
                print(delimeter.join(str(x) for x in i), file=file)

if __name__ == "__main__":
    stk = STK()
    stk.write(stk.run())
