#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This source defines analysis operation that aren't related to graphs.
"""

from __future__ import print_function

import numpy as np
import sys

deprecated_stop = True
deprecated_warn = False


def deprecated(func):
    def raise_exception(*args, **kwargs):
        if deprecated_stop: 
            raise DeprecationWarning(func.__name__ + " is deprecated, update code.")
        global deprecated_warn
        if not deprecated_warn:
            print(func.__name__ + " is deprecated, update code.", file=sys.stderr)
            deprecated_warn = True
        return func(*args, **kwargs)
    raise_exception.__name__ = func.__name__
    return raise_exception


def overlap_similarity(features1, features2):
    """Returns the overlap similarity from features of 2 nodes.
    
    Args:
        features1 (list): list of traits values from a node.
        features2 (list): list of traits values from another node."""
    curr_sum = 0
    for i in range(len(features1)):
        if features1[i] == features2[i]:
            curr_sum += 1
    return curr_sum/float(len(features1))
    

def get_different_trait_index(features1, features2):
    """Returns the index of a random trait that is different - IT MUST HAVE A LEAST ONE
    
    Args:
        features1 (list): list of traits values from a node.
        features2 (list): list of traits values from another node."""
    while True:
        test = np.random.randint(len(features1))
        if features1[test] != features2[test]:
            return test


@deprecated
def get_cultural_groups(population):
    """Returns the amount of cultural groups.
    
    Args:
        population (list of list): the features and traits of the population."""
    checked = set()
    for i in population:
        checked.add(tuple(i))
    return len(checked)


# MULTIPLE LAYERS #
def overlap_similarity_layer(features1, features2, curr_layer, amount_layers):
    """Returns the overlap similarity from features of 2 nodes in mutilayer.
    
    Args:
        features1 (list): list of traits values from a node.
        features2 (list): list of traits values from another node.
        curr_layer (int): the current layer being operated.
        amount_layers (int): the total amount of layers.
        
    Note:
        The behaviour becomes strange for non-divisible number of features by amount of layers."""
    layer_size = len(features1)/amount_layers
    curr_sum = 0
    for i in range(int(layer_size*curr_layer), int(layer_size*(curr_layer+1))):
        if features1[i] == features2[i]:
            curr_sum += 1
    return curr_sum/(float(len(features1))/amount_layers)


@deprecated
def get_cultural_groups_layer(population, curr_layer, amount_layers):
    """Returns the amount of cultural groups considering only a layer.
    
    Args:
        population (list of list): the features and traits of the population.
        curr_layer (int): the current layer being operated.
        amount_layers (int): the total amount of layers."""
    layer_size = len(population[0])/amount_layers
    checked = set()
    for i in population:
        checked.add(tuple(i[layer_size*curr_layer:layer_size*(curr_layer+1)]))
    return len(checked)


def get_cultural_groups_distribution(population, traits, gama=None):
    """Returns the distribution of node traits.
    
    Args:
        population (list of list): the features and traits of the population.
        traits (int): the amount of traits of the current graph.
        gama (number): the gama used for the current graph generation."""
    val = dict()
    d = _get_power_law_distribution(traits, gama)

    for node in population:
        for i in node:
            for k in range(len(d)):
                if i <= d[k]:
                    val[k] = val.get(k, 0) + 1
                    break
    result = list(val)
    result.sort()
    return result
