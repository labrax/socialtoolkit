# -*- coding: utf-8 -*-

"""
This source defines analysis related to cultural groups.
"""


import networkx as nx
from math import sqrt
import bisect


"""These are functions considering the topology of the graph."""


def _plain_bfs(graph, population, is_grid, num_side, source, source_features):
    seen = set()
    amt = 0
    nextlevel = {source}
    while nextlevel:
        thislevel = nextlevel
        nextlevel = set()
        for v in thislevel:
            if is_grid:
                this_features = population[v[0] * num_side + v[1]]
            else:
                this_features = population[v]
            if v not in seen and (this_features == source_features).all():
                seen.add(v)
                amt += 1
                nextlevel.update(graph[v])
    return amt, seen


def get_info_cultural_groups_topology(graph, population):
    """Returns a list with the sizes of each physical group.

    Args:
        graph (networkx.classes.graph): the graph.
        population (list of list): the features and traits of the population."""
    if nx.info(graph).split('\n')[0][6:] == 'grid_2d_graph':
        is_grid = True
        num_side = int(sqrt(len(graph)))
    else:
        is_grid = False
        num_side = None
    sizes = list()
    seen = set()
    for v in graph:
        if v not in seen:
            if is_grid:
                features = population[v[0] * num_side + v[1]]
            else:
                features = population[v]

            (amt, c) = _plain_bfs(graph, population, is_grid, num_side, v, features)
            bisect.insort_left(sizes, (amt, tuple(features)))
            seen.update(c)
    return sizes

"""These are functions considering groups that the graph topology doesn't matter."""


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
    layer_size = len(population[0]) / amount_layers
    checked = {}
    for i in population:
        checked[tuple(i[layer_size * curr_layer: layer_size * (curr_layer + 1)])] = \
            checked.get(tuple(i[layer_size * curr_layer: layer_size * (curr_layer + 1)]), 0) + 1
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
