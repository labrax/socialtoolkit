# -*- coding: utf-8 -*-

"""
This source defines analysis related to cultural groups.
"""

def _cultural_groups(population):
    checked = {}
    for i in population:
        checked[tuple(i)] = checked.get(tuple(i), 0) + 1
    return checked


def get_size_biggest_cultural_groups(population):
    """Returns the size of the biggest cultural group.

    Args:
        population (list of list): the features and traits of the population."""
    return max(_cultural_groups(population).values())


def get_amount_cultural_groups(population):
    """Returns the amount of cultural groups.

    Args:
        population (list of list): the features and traits of the population."""
    return len(_cultural_groups(population))


def get_info_cultural_groups(population):
    """Returns the amount of cultural groups and the biggest one.

    Args:
        population (list of list): the features and traits of the population."""
    info = _cultural_groups(population)
    return len(info), max(info.values())

"""Multilayers below"""
def _cultural_groups_layer(population, curr_layer, amount_layers):
    layer_size = len(population[0] ) /amount_layers
    checked = {}
    for i in population:
        checked[tuple(i[ layer_size *curr_layer: layer_size *( curr_layer +1)])] = \
            checked.get(tuple(i[ layer_size *curr_layer: layer_size *( curr_layer +1)]), 0) + 1
    return checked


def get_size_biggest_cultural_groups_layer(population, curr_layer, amount_layers):
    """Returns the size of the biggest cultural group considering only a layer.

    Args:
        population (list of list): the features and traits of the population.
        curr_layer (int): the current layer being operated.
        amount_layers (int): the total amount of layers."""
    return max(_cultural_groups_layer(population, curr_layer, amount_layers).values())


def get_amount_cultural_groups_layer(population, curr_layer, amount_layers):
    """Returns the amount of cultural groups considering only a layer.

    Args:
        population (list of list): the features and traits of the population.
        curr_layer (int): the current layer being operated.
        amount_layers (int): the total amount of layers."""
    return len(_cultural_groups_layer(population, curr_layer, amount_layers))


def get_info_cultural_groups_layer(population, curr_layer, amount_layers):
    """Returns the amount of cultural groups and the biggest one considering only a layer.

    Args:
        population (list of list): the features and traits of the population.
        curr_layer (int): the current layer being operated.
        amount_layers (int): the total amount of layers."""
    info = _cultural_groups_layer(population, curr_layer, amount_layers)
    return len(info), max(info.values())