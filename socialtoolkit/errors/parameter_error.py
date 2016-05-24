#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The source has the error for parameters.
"""


class ParameterError(Exception):
    def __init__(self, val, explanation, variables):
        output = "{0}\n{1}\nVariables: ".format(val, explanation)  # val + "\n" + explanation + "\n"
        for i in range(0, len(variables.items())):
            output += "'{0}' : {1}".format(str(variables.items()[i][0]), str(variables.items()[i][1]))
            if i < len(variables.items())-1:
                output += ", "
        output += "."
        super(ParameterError, self).__init__(output)
