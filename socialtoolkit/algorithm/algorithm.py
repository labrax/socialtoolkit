#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

class Algorithm(object):
    def __lt__(self, other):
        return id(self) < id(other)
