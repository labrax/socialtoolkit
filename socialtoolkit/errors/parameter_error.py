#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The source has the error for parameters.
"""


class ParameterError(Exception):
    def __init__(self, val, explanation, variables):
        output = "{0}\n{1}\nVariables: ".format(val, explanation)  # val + "\n" + explanation + "\n"
        all_items = list(variables.items())
        for i in range(0, len(all_items)):
            output += "'{0}' : {1}".format(str(all_items[i][0]), str(all_items[i][1]))
            if i < len(variables.items())-1:
                output += ", "
        output += "."
        super(ParameterError, self).__init__(output)
