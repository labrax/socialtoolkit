#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This source defines basic structure for analysis algorithms.
"""

from ..algorithm import Algorithm

class AnalysisAlgorithm(Algorithm):
    """Base class for anaysis algorithms."""
    def __init__(self, first, step, function, data):
        """Args:
            first (int): the first iteration to analyse.
            step (int): the increment to analysis runs.
            function (function): the method to run the analysis.
            data (list): the parameters for the method."""
        self._next = first
        self._step = step
        self._results = []
        self._function = function
        self._data = data
    def next(self):
        """Returns when will be the next analysis iteration."""
        return self._next
    def get_results(self):
        """Returns the vector of results."""
        return self._results
    def step(self):
        """Dummy: do nothing - to be implemented on children classes."""
        pass

class CommandAnalysis(AnalysisAlgorithm):
    """This type of analysis run a method to run the analysis."""
    def __init__(self, first, step, function, data):
        super(CommandAnalysis, self).__init__(first, step, function, data)
    def step(self, index):
        """Run the analysis and returns the index of next iteration to be analysed.
        
        Args:
            index (int): the index of current iteration."""
        self._results.append((index, self._function(*self._data)))
        if self._step > 0:
            self._next += self._step
        return self._next

class AmountIterationLayerAnalysis(AnalysisAlgorithm):
    """This analysis obtains the number of iterations for each layer."""
    def __init__(self, data, layers):
        super(AmountIterationLayerAnalysis, self).__init__(0, 0, None, data)
        self._results = [0] * layers
    def step(self, index):
        """Increment the layer count and returns the index of next iteration to be analysed.
        
        Args:
            index (int): the index of current iteration."""
        self._results[self._data[0]] += 1
        self._next = index+1
        return self._next
