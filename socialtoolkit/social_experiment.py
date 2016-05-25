#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This source defines the workings of a simulation using the toolkit.
"""

try:
    from queue import PriorityQueue
except:
    from Queue import PriorityQueue
import numpy.random as random


class Experiment(object):
    """The base experiment class."""
    def __init__(self, network, evolution_algorithm, convergence, **parameters):
        """Initiates an experiment.

        Args:
            network (socialtoolkit.graph.network): the network with graph and features/traits information.
            evolution_algorithm (socialtoolkit.algorithm.evolution.evolution_algorithm generator): the evolution generator.
            convergence (socialtoolkit.algorithm.convergence): the convergence criteria for the experiment."""
        if network:
            self._G = network.graph
            self._population = network.population_data
        if evolution_algorithm:
            if evolution_algorithm.__name__ == "Klemm":
                self._model = evolution_algorithm(self._G, self._population, parameters['traits'], parameters['klemm_rate'])
            else:
                self._model = evolution_algorithm(self._G, self._population)
        self._convergence = convergence
        self._queue = PriorityQueue()
        self.iterate = self._iterate_no_step_analysis
        self._analysis = None
        self.i = 0

    def add_analysis(self, analysis):
        """Adds an analysis to the experiment.
        
        Args:
            analysis (socialtoolkit.algorithm.analysis.analysis): the analysis algorithm."""
        self._analysis = analysis
        for i in analysis:
            self._queue.put((i.next(), i))
        self.iterate = self._iterate_step_analysis

    def converge(self):
        """Run until convergence."""
        self.i = 0
        while not self._convergence.is_done():
            self.iterate()
        while not self._queue.empty():
            e = self._queue.get()
            e[1].step(self.i)
        return self.i

    def iterate(self):
        pass

    def _iterate_step_analysis(self):
        """Run an iteration."""
        # if self.i % 10**3 == 0:
        #     print self.i
        # if not self._queue.empty():
        while not self._queue.empty() and self._queue.queue[0][0] <= self.i:
            e = self._queue.get()
            if e[1].step(self.i) != self.i:
                self._queue.put((e[1].next(), e[1]))
        self._convergence.update(self.i, self._model.iterate())
        self.i += 1

    def _iterate_no_step_analysis(self):
        self._convergence.update(self.i, self._model.iterate())
        self.i += 1


class EqualMultilayerExperiment(Experiment):
    """The experiment class for multilayer."""
    def __init__(self, network, evolution_algorithm, convergence, layers, **parameters):
        """Initiates an experiment.
        
        Args:
            network (socialtoolkit.grpah.network): the network with graph and features/traits information.
            population (list of list): of features and traits of the population.
            evolution_algorithm (socialtoolkit.algorithm.evolution.evolution_algorithm generator): the evolution generator.
            convergence (socialtoolkit.algorithm.convergence): the convergence criteria for the experiment.
            layers (int): the amount of layers."""
        super(EqualMultilayerExperiment, self).__init__(network, None, convergence)
        self.all_G = network.graph
        self.all_model = []
        for i in network.graph:
            if evolution_algorithm.__name__ == "Klemm" or evolution_algorithm.__name__ == "MultilayerKlemm":
                self.all_model.append(evolution_algorithm(i, self._population, parameters['traits'], parameters['klemm_rate']))
            else:
                self.all_model.append(evolution_algorithm(i, self._population))
        self._curr = [0]

    def converge(self):
        """Run until convergence.
        
        Note: this method changes the current graph on the run."""
        self.i = 0
        while not self._convergence.is_done():
            self._curr[0] = random.randint(len(self.all_G))
            self._G = self.all_G[self._curr[0]]
            self._model = self.all_model[self._curr[0]]
            self.iterate()
        while not self._queue.empty():
            e = self._queue.get()
            e[1].step(self.i)
        return self.i
