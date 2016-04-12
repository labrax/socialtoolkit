#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

from ..algorithm import Algorithm

class AnalysisAlgorithm(Algorithm):
    pass

class CommandAnalysis(AnalysisAlgorithm):
    def __init__(self, first, step, function, data):
        self._next = first
        self._step = step
        self._results = []
        self._function = function
        self._data = data
    def next(self):
        return self._next
    def get_results(self):
        return self._results
    def step(self, index):
        self._results.append((index, self._function(*self._data)))
        if self._step > 0:
            self._next += self._step
        return self._next

class AmountIterationLayerAnalysis(CommandAnalysis):
    def __init__(self, data, layers):
        super(AmountIterationLayerAnalysis, self).__init__(0, 0, None, data)
        self._results = [0] * layers
    def step(self, index):
        self._results[self._data[0]] += 1
        self._next = index+1
        return self._next
