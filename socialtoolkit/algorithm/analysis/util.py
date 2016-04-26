#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This source defines analysis operation that aren't related to graphs.
"""

import numpy as np

def overlap_similarity(features1, features2):
    """Returns the overlap similarity from features of 2 nodes.
    
    Args:
        features1 (list): list of traits values from a node.
        features2 (list): list of traits values from another node."""
    sum = 0
    for i in range(len(features1)):
        if features1[i] == features2[i]:
            sum += 1
    return sum/float(len(features1))
    
def get_different_trait_index(features1, features2):
    """Returns the index of a random trait that is different - IT MUST HAVE A LEAST ONE
    
    Args:
        features1 (list): list of traits values from a node.
        features2 (list): list of traits values from another node."""
    while True:
        test = np.random.randint(len(features1))
        if(features1[test] != features2[test]):
            return test

def get_cultural_groups(population):
    """Returns the amount of cultural groups.
    
    Args:
        population (list of list): the features and traits of the population."""
    checked = set()
    for i in population:
        checked.add(tuple(i))
    return len(checked)

###### MULTIPLE LAYERS #####
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
    sum = 0
    for i in range(int(layer_size*curr_layer), int(layer_size*(curr_layer+1))):
        if features1[i] == features2[i]:
            sum += 1
    return sum/(float(len(features1))/amount_layers)

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
