#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

import sys
try:
    from queue import PriorityQueue
except:
    from Queue import PriorityQueue
import numpy.random as random

class Experiment(object):
    def __init__(self, G, population, evolution_algorithm, convergence):
        if G:
            self._G = G[0](*G[1])
        self._population = population[0](*population[1])
        if evolution_algorithm:
            self._model = evolution_algorithm(self._G, self._population)
        self._convergence = convergence
        self._queue = PriorityQueue()
    def add_analysis(self, analysis):
        self._analysis = analysis
        for i in analysis:
            self._queue.put((i.next(), i))
    def converge(self):
        self.i = 1
        while not self._convergence.is_done():
            self.iterate()
        return self.i
    def iterate(self):
        #if self.i % 10**3 == 0:
            #print self.i
        while not self._queue.empty() and self._queue.queue[0][0] <= self.i:
            e = self._queue.get()
            if e[1].step(self.i) != self.i:
                self._queue.put((e[1].next(), e[1]))
        self._convergence.update(self.i, self._model.iterate())
        self.i = self.i + 1

class EqualMultilayerExperiment(Experiment):
    def __init__(self, G, population, evolution_algorithm, convergence, layers):
        super(EqualMultilayerExperiment, self).__init__(None, population, None, convergence)
        self.all_G = []
        self.all_model = []
        for i in G:
            curr = i[0](*i[1])
            self.all_G.append(curr)
            self.all_model.append(evolution_algorithm(curr, self._population))
        self._curr = [0]
    def converge(self):
        self.i = 1
        while not self._convergence.is_done():
            self._curr[0] = random.randint(len(self.all_G))
            self._G = self.all_G[self._curr[0]]
            self._model = self.all_model[self._curr[0]]
            super(EqualMultilayerExperiment, self).iterate()
        return self.i
