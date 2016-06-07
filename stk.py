#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The source has the initializer for running the socialtoolkit.
"""

from __future__ import print_function

import argparse
from multiprocessing import cpu_count
from time import ctime
import sys
from socialtoolkit.errors.parameter_error import ParameterError
from socialtoolkit.worker import valid_algorithms


def work_stk(parameters):
    from socialtoolkit.worker import work
    return work(parameters)


class STK:
    def __init__(self):
        self.run_id = ctime().replace(' ', '_')
        self.args = self.__process_args()

        if type(self.args.layers) == list:
            self.args.layers = self.args.layers[0]

        self.args.algorithm = self.__algorithm_name_check(self.args.algorithm)

        self.global_headers = dict()
        self.result = None

        self.args.gridsize = self.__process_range(self.args.gridsize)
        self.args.traits = self.__process_range(self.args.traits)
        self.args.features = self.__process_range(self.args.features)
        self.args.klemm_rate = self.__process_range(self.args.klemm_rate)

        if self.args.auto_output:
            self.output = self.__run_name(self.args)
            self.global_output = "global_" + self.output
        else:
            self.output = sys.stdout
            self.global_output = sys.stderr

        # fix for int/str in list values
        if type(self.args.convergence_max_iterations) == list:
            self.args.convergence_max_iterations = self.args.convergence_max_iterations[0]
        if type(self.args.convergence_step_check) == list:
            self.args.convergence_step_check = self.args.convergence_step_check[0]
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
        if self.args.analysis_step != 0 or self.args.population_output or self.args.graph_output:
            self.__prepare_dir(self.args.output_dir)
        if type(self.args.repeat) == list:
            self.args.repeat = self.args.repeat[0]

        if len(self.args.gridsize) == 0 or self.args.gridsize[0] < 0:
            raise ParameterError("Interval for gridsize invalid.", "Interval must be with numbers above or equal to 1!",
                                 {'gridsize': self.args.gridsize})
        if len(self.args.traits) == 0 or self.args.traits[0] < 0:
            raise ParameterError("Interval for traits invalid.", "Interval must be with numbers above or equal to 1!",
                                 {'traits': self.args.traits})
        if len(self.args.features) == 0 or self.args.features[0] < 0:
            raise ParameterError("Interval for features invalid.", "Interval must be with numbers above or equal to 1!",
                                 {'traits': self.args.features})
        if len(self.args.klemm_rate) == 0 or self.args.klemm_rate[0] < 0:
            raise ParameterError("Interval for Klemm rate invalid.", "Interval must be with numbers above or equal to 0!",
                                 {'traits': self.args.klemm_rate})

        # conflicts section
        if self.args.graph_input is not None and len(self.args.gridsize) > 1:
            raise ParameterError("Can't load a graph and use multiple gridsizes.", "When using a loaded graph don't set a range for gridsize!", {'gridsize' : len(self.args.gridsize), 'graph_input' : self.args.graph_input})
        if self.args.population_input is not None and (len(self.args.traits) > 1 or len(self.args.features) > 1):
            raise ParameterError("Can't load a population file and use information.", "When using a loaded population file don't set a range for features or traits!", {'features' : len(self.args.features), 'traits' : len(self.args.traits), 'population_input' : self.args.population_input})

        # incoherent values
        if self.args.analysis_step < 0:
            raise ParameterError("Interval for analysis step invalid.", "Interval for analysis step must be an integer above or equal to 1!", {'repeat': self.args.analysis_step})
        if self.args.repeat <= 0:
            raise ParameterError("Number of repeats invalid.", "Number of repeats must be an integer equal or above 1!", {'repeat' : self.args.repeat})

        # store all the parameters for execution
        self.all_P = self.__exec_params(self.args)

        self.headers = None

    def __process_args(self):
        """Return the processed arguments."""
        parser = argparse.ArgumentParser(
            description="Execute a simulation for a generated network and properties using a social algorithm." +
                        "The ranges can be written as values to iterate in between (2 or 3 arguments)" +
                        " or as a list of elements.")
        # base configuration
        parser.add_argument('-gs', '--gridsize', metavar='N', default=32, type=int, nargs='+',
                            help='a range for the gridsize')
        parser.add_argument('-t', '--traits', metavar='N', default=3, type=int, nargs='+',
                            help='a range for the traits')
        parser.add_argument('-f', '--features', metavar='N', default=5, type=int, nargs='+',
                            help='a range for the features')
        parser.add_argument('-l', '--layers', metavar='N', default=1, type=int, nargs=1,
                            help='a number of layers')
        parser.add_argument('-A', '--algorithm', metavar='<algorithm>', default="axelrod", type=str, nargs=1,
                            help='an simulation algorithm, "axelrod", "centola" or "kleem"')
        # klemm rate
        parser.add_argument('-K', '--klemm-rate', metavar='N', dest='klemm_rate', default=0.01, type=float, nargs='+',
                            help="value for Klemm's rate of perturbation")
        # convergence settings
        parser.add_argument('-cI', '--convergence-max-iterations', metavar='N', default=150*10**6, type=int, nargs=1,
                            help='maximum number of iterations')
        parser.add_argument('-cS', '--convergence-step-check', metavar='N', default=10**4, type=int, nargs=1,
                            help='step for convergence check')
        # multithreading
        parser.add_argument('--spark', metavar='SPARK', const="spark://10.1.1.28:7077", type=str, nargs='?',
                            help='connect using spark')
        parser.add_argument('--threads', metavar='THREADS', dest='threads', default=cpu_count(), type=int, nargs=1,
                            help='set the number of threads - default on this machine ' + str(cpu_count()))
        # analysis settings
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
        # analysis step-by-step
        parser.add_argument('-SA', '--analysis-step', metavar='N', dest='analysis_step', default=0, type=int, nargs=1,
                            help='an interval for the analysis')
        parser.add_argument('-OA', '--analysis-output', metavar='OUTPUT-DIR', dest='output_dir', default="/userdata/vroth/output_data/run_" + str(self.run_id), type=str, nargs=1,
                            help='a folder for the output of analysis')
        # input files for graph and population
        parser.add_argument('-IP', '--input-population', metavar='POPULATION-INPUT-FILE', dest='population_input', type=str, nargs=1,
                            help='an input population file')
        parser.add_argument('-IG', '--input-graph', metavar='GRAPH-INPUT-FILE', dest='graph_input', type=str, nargs=1,
                            help='an input graph file')
        parser.add_argument('-OP', '--output-population', metavar='POPULATION-OUTPUT', dest='population_output',
                            action='store_const', const=True, default=False,
                            help='an output population file')
        parser.add_argument('-OG', '--output-graph', metavar='GRAPH-OUTPUT', dest='graph_output',
                            action='store_const', const=True, default=False,
                            help='an output graph file')
        # other settings
        parser.add_argument('-R', '--repeat', metavar='N', dest='repeat', default=1, type=int, nargs=1,
                            help='number of runs for each setting')
        parser.add_argument('--auto-output', metavar='AUTO-OUTPUT', dest='auto_output',
                            action='store_const', const=True, default=False,
                            help='auto generate output file given input settings')
        args = parser.parse_args()
        return args

    def __run_name(self, args):
        if len(args.gridsize) == 1:
            gridsize = args.gridsize[0]
        elif len(args.gridsize) == 2:
            gridsize = "{0}_{1}".format(args.gridsize[0], args.gridsize[1])
        elif len(args.gridsize) == 3:
            gridsize = "{0}_{1}__{2}".format(args.gridsize[0], args.gridsize[1], args.gridsize[2])
        else:
            gridsize = "list{0}_to_{1}".format(args.gridsize[0], args.gridsize[-1])
        if len(args.traits) == 1:
            traits = args.traits[0]
        elif len(args.traits) == 2:
            traits = "{0}_{1}".format(args.traits[0], args.traits[1])
        elif len(args.traits) == 3:
            traits = "{0}_{1}__{2}".format(args.traits[0], args.traits[1], args.traits[2])
        else:
            traits = "list{0}_to_{1}".format(args.traits[0], args.traits[-1])
        if len(args.features) == 1:
            features = args.features[0]
        elif len(args.features) == 2:
            features = "{0}_{1}".format(args.features[0], args.features[1])
        elif len(args.features) == 3:
            features = "{0}_{1}__{2}".format(args.features[0], args.features[1], args.features[2])
        else:
            features = "list{0}_to_{1}".format(args.features[0], args.features[-1])
        if len(args.klemm_rate) == 1:
            klemm_rate = args.klemm_rate[0]
        elif len(args.features) == 2:
            klemm_rate = "{0}_{1}".format(args.klemm_rate[0], args.klemm_rate[1])
        elif len(args.features) == 3:
            klemm_rate = "{0}_{1}__{2}".format(args.klemm_rate[0], args.klemm_rate[1], args.klemm_rate[2])
        else:
            klemm_rate = "list{0}_to_{1}".format(args.klemm_rate[0], args.klemm_rate[-1])
        if type(self.args.layers) == list:
            layers = self.args.layers[0]
        else:
            layers = self.args.layers
        return "simulation_{5}_gs{0}_f{1}_t{2}_l{3}_k{6}_{4}.csv".format(
            gridsize, features, traits, layers, self.args.algorithm, self.run_id, klemm_rate)

    def __process_range(self, val):
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

    def __algorithm_name_check(self, val):
        """Returns the algorithm function for the program argument.
        
        Args:
            val (str or list): the name of the class."""
        if type(val) == list:
            val = val[0]
        val = val.lower()
        if val not in valid_algorithms:
            raise ParameterError("Invalid name of algorithm.", "Algorithm must be either {0} or {1}!".format(", ".join([x.capitalize() for x in valid_algorithms[:-1]]), valid_algorithms[-1].capitalize()), {'given algorithm': val})
        return val

    def __exec_params(self, args):
        """Returns the list of parameters for execution.
        
        Args:
            args (Namespace): the processed arguments of the program."""
        all_p = list()

        global_parameters = dict()
        global_parameters['algorithm'] = args.algorithm
        global_parameters['max_iterations'] = args.convergence_max_iterations
        if global_parameters['max_iterations'] == 0:
            global_parameters['max_iterations'] = 150*(10**4)
        global_parameters['step_check'] = args.convergence_step_check
        global_parameters['layers'] = args.layers

        if args.physical is False and args.cultural is False and args.biggest_physical is False and args.biggest_cultural is False:
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

        global_parameters['graph_output'] = args.graph_output
        global_parameters['population_output'] = args.population_output

        self.global_headers = global_parameters.copy()
        self.global_headers['repeat'] = args.repeat
        if len(args.gridsize) == 1:
            self.global_headers['width'] = args.gridsize[0]
            self.global_headers['height'] = args.gridsize[0]
        if len(args.traits) == 1:
            self.global_headers['traits'] = args.traits[0]
        if len(args.features) == 1:
            self.global_headers['features'] = args.features[0]
        if len(args.klemm_rate) == 1:
            self.global_headers['klemm_rate'] = args.klemm_rate[0]

        # generate all the parameters
        for r in range(args.repeat):
            for gs in args.gridsize:
                for t in args.traits:
                    for f in args.features:
                        for k in args.klemm_rate:
                            if f % args.layers != 0:
                                # raise ParameterError("Invalid relation of features and layers.", "Features must be divisible by layers!", {'features' : f, 'layers' : args.layers})
                                print("Invalid relation of features and layers.\nFeatures must be divisible by layers! Skipping features and layers: ", f, self.args.layers, file=sys.stderr)
                                continue

                            parameters = dict()
                            parameters['width'] = gs
                            parameters['height'] = gs
                            parameters['features'] = f
                            parameters['traits'] = t
                            parameters['repeat'] = r
                            parameters['global_parameters'] = global_parameters
                            parameters['klemm_rate'] = k
                            all_p.append(parameters)
        return all_p

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
        # run case for spark
        if self.args.spark:
            from pyspark import SparkContext, SparkConf
            conf = SparkConf().setAppName("social_simulations_" + str(self.run_id)).setMaster(self.args.spark)  # .set("spark.eventLog.enabled", "false").set("spark.shuffle.service.enabled.", "true").set("spark.dynamicAllocation.enabled", "true")  # .set("spark.python.profile", "true")
            sc = SparkContext(conf=conf)  # ('local', 'test')
            sc.setLogLevel("WARN")
            sc.addPyFile("util/socialtoolkit.zip")
            ratios_rdd = sc.parallelize(self.all_P, len(self.all_P))
            prepared_work = ratios_rdd.map(work_stk)
            result = prepared_work.collect()
        else:
            if len(self.all_P) < self.args.threads:
                amount_process = len(self.all_P)
            else:
                amount_process = self.args.threads

            if amount_process > 1:
                # run with multiple processes
                from socialtoolkit.local_worker_manager import run
                result = run(amount_process, work_stk, self.all_P)
            else:
                # run in a single process
                for i in self.all_P:
                    result.append(work_stk(i))
        self.result = result

    def get_headers(self):
        if hasattr(self, "headers") and self.headers is not None:
            return self.headers
        self.headers = ["algorithm", "width", "height", "layers", "features", "traits", "convergence_max_iterations",
                        "convergence_step_check", "convergence_iterations", "convergence_time"]
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

    def write_global_data(self, target=sys.stdout):
        if type(target) == str:
            target = open(target, "w")
        values = list(self.global_headers.iteritems())
        values.sort()
        for i,j in values:
            if i is None:
                print("invalid value", file=sys.stderr)
            else:
                print(i, j, file=target)

    def get_fields_to_print(self):
        important_outputs = ["algorithm", "max_iterations", "step_check", "analysis_step", "layers", "graph_input",
                             "population_input", "width", "height", "traits", "features", "klemm_rate",
                             "graph_output", "population_output"]
        will_be_printed = list()
        for i in important_outputs:
            if i not in self.global_headers:
                will_be_printed.append(i)
        if self.global_headers['cultural'] == True:
            will_be_printed.append("amount_cultural_groups")
        if self.global_headers['biggest_cultural'] == True:
            will_be_printed.append("biggest_cultural_group")
        if self.global_headers['physical'] == True:
            will_be_printed.append("amount_physical_groups")
        if self.global_headers['biggest_physical'] == True:
            will_be_printed.append("biggest_physical_group")

        if self.args.layers > 1:
            for i in range(self.args.layers):
                will_be_printed.append("amount_cultural_groups" + str(i))
                will_be_printed.append("biggest_cultural_group" + str(i))
                will_be_printed.append("amount_physical_groups" + str(i))
                will_be_printed.append("biggest_physical_group" + str(i))
        return will_be_printed

    def write_selecting(self, print_list, delimeter=',', target=sys.stdout):
        if type(target) == str:
            target = open(target, "w")
        print(delimeter.join(str(i) for i in print_list), file=target)
        for i in self.result:
            if i is None:
                print("invalid value", file=sys.stderr)
            else:
                valid_values = list()
                for elem in print_list:
                    if elem in i:
                        valid_values.append(i[elem])
                    else:
                        valid_values.append("-")
                print(delimeter.join(str(x) for x in valid_values), file=target)

    def write(self, delimeter=',', target=sys.stdout):
        if type(target) == str:
            target = open(target, "w")
        print(delimeter.join(str(i) for i in self.get_headers()), file=target)
        for i in self.result:
            if i is None:
                print("invalid value", file=sys.stderr)
            else:
                print(delimeter.join(str(x) for x in i.values()), file=target)

if __name__ == "__main__":
    stk = STK()
    if stk.output != sys.stdout:
        print("output to:", stk.output)
    stk.run()
    stk.write_global_data(stk.global_output)
    stk.write_selecting(stk.get_fields_to_print(), target=stk.output)
    #stk.write(target=stk.output)
