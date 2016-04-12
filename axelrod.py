#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

from model import Model
from util import overlap_similarity, get_different_trait_index

import numpy.random as random
from random import choice

import networkx as nx

class Axelrod(Model):
    def __init__(self, G, population):
        super(Axelrod, self).__init__(G, population)
    def iterate(self):
        active, passive, neighbors, features_active, features_passive = super(Axelrod, self).pre_iteration()
        s = overlap_similarity(features_active, features_passive)
        if s > 0 and s < 1:
            if random.random() < s:
                i =  get_different_trait_index(features_active, features_passive)
                features_active[i] = features_passive[i]
                return True
