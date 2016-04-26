#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

class Algorithm(object):
    """Base class for defining algorithms."""
    def __lt__(self, other):
        return id(self) < id(other)
