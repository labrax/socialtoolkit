#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

import numpy as np

def overlap_similarity(features1, features2):
    """compute overlap similarity of features from 2 nodes"""
    sum = 0
    for i in range(len(features1)):
        if features1[i] == features2[i]:
            sum += 1
    return sum/float(len(features1))
    
def get_different_trait_index(features1, features2):
    """return the index of a random trait that is different - IT MUST HAVE A LEAST ONE"""
    while True:
        test = np.random.randint(len(features1))
        if(features1[test] != features2[test]):
            return test

def get_cultural_groups(population):
    checked = set()
    for i in population:
        checked.add(tuple(i))
    return len(checked)

###### MULTIPLE LAYERS #####
def overlap_similarity_layer(features1, features2, curr_layer, amount_layers):
    """compute overlap similarity of features from 2 nodes"""
    layer_size = len(features1)/amount_layers
    sum = 0
    for i in range(int(layer_size*curr_layer), int(layer_size*(curr_layer+1))):
        if features1[i] == features2[i]:
            sum += 1
    return sum/float(len(features1)/amount_layers)

def get_cultural_groups_layer(population, curr_layer, amount_layers):
    layer_size = len(population[0])/amount_layers
    checked = set()
    for i in population:
        checked.add(tuple(i[layer_size*curr_layer:layer_size*(curr_layer+1)]))
    return len(checked)
