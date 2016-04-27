#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This source defines a unified class for output printing with variable arguments.
"""

from __future__ import print_function

import sys
try:
    from queue import PriorityQueue
except:
    from Queue import PriorityQueue
from .analysis import AnalysisAlgorithm

class OutputAnalysis:
    """Class for output of analysis"""
    def __init__(self, analysis, headers=[], delimeter=',', output=sys.stdout):
        """Args:
            analysis (list/AnalysisAlgorithm instance or list of AnalysisAlgorithm instances): the analysis ran.
            headers (list of str): the name for each output column.
            delimeter (Optional[str]): the delimeter for the output.
            output (file name or channel): the output file or channel.
            
        Note:
            If the output filename is a file that already exists it will be removed and re-created."""
        self.analysis = []
        if type(analysis) == list and isinstance(analysis[0], AnalysisAlgorithm): #many analysis
            for i in analysis:
                self.analysis.append(i.get_results())
        elif isinstance(analysis, AnalysisAlgorithm): #only one analysis
            self.analysis = analysis.get_results()
        else: #is a list of results
            self.analysis = analysis
        self.headers = headers
        self.delimeter = delimeter
        if type(output) == str: #if is a string name opens the file for writing
            try:
                self.output = open(output, "w")
            except Exception as e:
                print(e, "thus using stdout", file=sys.stderr)
                self.output = sys.stdout
        else:
            self.output = output
    def __exit__(self):
        """Upon exit close file handler if needed."""
        if type(self.output).__name__ == 'file':
            self.output.close()
    def write(self):
        """Print all output."""
        if type(self.headers) == str: #if the header is a str
            self.output.write(str(self.headers) + '\n')
        elif self.headers:
            if type(self.headers[0]) == str: #or as list of string
                output = self.headers[0]
            else: #or as list of functions
                output = self.headers[0].__name__
            for h in self.headers[1:]: #the remaining of the list
                if type(h) == str:
                    output += self.delimeter + h
                else:
                    output += self.delimeter + h.__name__
            output += '\n'
            self.output.write(output)

        if type(self.analysis[0]) == type([]): #multiple analysis
            queue = PriorityQueue()
            
            curr_index = self.analysis[0][0][1]
            curr_values = ['0'] * len(self.analysis)
            
            for a in range(0, len(self.analysis)):
                queue.put((self.analysis[a][0][0], a, 0))
                if curr_index > self.analysis[a][0][0]:
                    curr_index = self.analysis[a][0][0]
            while not queue.empty(): #print all the values, filling with previous data
                e = queue.get()
                if e[0] != curr_index:
                    self.output.write(str(curr_index) + self.delimeter + self.delimeter.join(curr_values) + '\n')
                    curr_index = e[0]
                curr_values[e[1]] = str(self.analysis[e[1]][e[2]][1])
                if e[2] < len(self.analysis[e[1]]) - 1:
                    queue.put((self.analysis[e[1]][e[2]+1][0], e[1], e[2]+1))
            self.output.write(str(e[0]) + self.delimeter + self.delimeter.join(curr_values) + '\n')
        elif type(self.analysis[0]) == type(tuple()): #data with tuple format
            for e in self.analysis:
                self.output.write(str(e[0]) + self.delimeter + str(e[1]) + '\n')
        else: #data with only values
            if len(self.analysis) == len(self.headers):
                output = str(self.analysis[0])
                for e in range(1, len(self.analysis)):
                    output += self.delimeter + str(self.analysis[e])
                self.output.write(output + '\n')
            else:
                for i in self.analysis:
                    self.output.write(str(i) + '\n')
