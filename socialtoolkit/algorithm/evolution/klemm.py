#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This source contains the Konstantin Kleem's cultural drift.
"""

from .axelrod import Axelrod
from math import sqrt
import numpy.random as random


class Klemm(Axelrod):
    def __init__(self, G, population, amount_traits, probability):
        self.probability = probability
        self.amount_traits = amount_traits
        super(Klemm, self).__init__(G, population)

    def iterate(self):
        if super(Klemm, self).iterate() or self.step_klemm():
            return True

    def step_klemm(self):
        if random.random() < self.probability:
            if self._grid:
                num_side = int(sqrt(self._nodes))
                active = (random.randint(num_side), random.randint(num_side))
                features_active = self.population[active[0]*int(sqrt(self._nodes)) + active[1]]
            else:
                active = random.randint(self._nodes)
                features_active = self.population[active]
            features_active[int(random.random()*len(features_active))] = int(random.random()*self.amount_traits)
            return True
