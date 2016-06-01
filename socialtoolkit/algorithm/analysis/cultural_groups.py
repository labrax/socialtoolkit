# -*- coding: utf-8 -*-

"""
This source defines analysis related to cultural groups.
"""


import networkx as nx
from math import sqrt
import bisect

"""These functions consider the topology of the graph."""


def _plain_bfs(graph, population, is_grid, num_side, source, source_features, first_feature, last_feature):
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
            if v not in seen and \
                    (this_features[first_feature:last_feature] == source_features[first_feature:last_feature]).all():
                seen.add(v)
                amt += 1
                nextlevel.update(graph[v])
    return amt, seen


def _cultural_groups_topology(network, first_feature=0, last_feature=-1):
    """
    Returns a list with the sizes of each physical group.
    :param network: the network data.
    """
    if last_feature == -1:
        last_feature = len(network.population_data[0])
    graph = network.graph[0]
    population = network.population_data
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
            (amt, c) = _plain_bfs(graph, population, is_grid, num_side, v, features, first_feature, last_feature)
            bisect.insort_left(sizes, (amt, tuple(features)))
            seen.update(c)
    return sizes


def get_size_biggest_cultural_groups_topology(network):
    """
    Returns the size of the biggest cultural group.
    :param network: the network data.
    :return: the size
    """
    return get_info_cultural_groups_topology(network)[-1][0]


def get_amount_cultural_groups_topology(network):
    """
    Return sthe amount of cultural groups.
    :param network: the network data.
    :return: the amount of cultural groups.
    """
    return len(get_info_cultural_groups_topology(network))


def get_info_cultural_groups_topology(network):
    """
    Returns the amount of cultural groups and the biggest one considering the topology.
    :param network: the network data.
    :return: the amount of cultural groups and the size of the biggest cultural group.
    """
    info = _cultural_groups_topology(network)
    return len(info), info[-1][0]

########################################################################################################################
"""Multilayer for the topology analysis"""


def get_size_biggest_cultural_groups_topology_layer(network, curr_layer):
    """
    Returns the size of the biggest cultural group.
    :param network: the network data.
    :param curr_layer: the layer under analysis.
    :return: the size of the biggest cultural group.
    """
    layer_size = len(network.population_data[0]) / network.layers
    return _cultural_groups_topology(network, int(layer_size * curr_layer), int(layer_size * (curr_layer + 1)))[-1][0]


def get_amount_cultural_groups_topology_layer(network, curr_layer):
    """
    Returns the amount of cultural groups.
    :param network: the network data.
    :param curr_layer: the layer under analysis.
    :return: the amount of cultural groups.
    """
    layer_size = len(network.population_data[0]) / network.layers
    return len(_cultural_groups_topology(network, int(layer_size * curr_layer), int(layer_size * (curr_layer + 1))))

########################################################################################################################
"""The functions below consider groups where the graph topology doesn't matter."""


def _cultural_groups(network):
    """
    Returns the cultural groups analysis data dictionary.
    :param network:
    :return:
    """
    checked = {}
    for i in network.population_data:
        checked[tuple(i)] = checked.get(tuple(i), 0) + 1
    return checked


def get_size_biggest_cultural_groups(network):
    """
    Returns the size of the biggest cultural group.
    :param network: the network data.
    """
    return max(_cultural_groups(network).values())


def get_amount_cultural_groups(network):
    """
    Returns the amount of cultural groups.
    :param network: the network data.
    """
    return len(_cultural_groups(network))


def get_info_cultural_groups(network):
    """
    Returns the amount of cultural groups and the biggest one.
    :param network: the network data.
    """
    info = _cultural_groups(network)
    return len(info), max(info.values())

########################################################################################################################
"""Multilayers below"""


def _cultural_groups_layer(network, curr_layer):
    """
    Returns the amount of cultural groups for a layer.
    :param network: the network data.
    :param curr_layer: the layer under analysis.
    :return: dictionary with data.
    """
    layer_size = len(network.population_data[0]) / network.layers
    checked = {}
    for i in network.population_data:
        checked[tuple(i[int(layer_size * curr_layer): int(layer_size * (curr_layer + 1))])] = \
            checked.get(tuple(i[int(layer_size * curr_layer): int(layer_size * (curr_layer + 1))]), 0) + 1
    return checked


def get_size_biggest_cultural_groups_layer(network, curr_layer):
    """
    Returns the size of the biggest cultural group considering only a layer.
    :param network: the network data.
    :param curr_layer: the layer under analysis.
    """
    return max(_cultural_groups_layer(network, curr_layer).values())


def get_amount_cultural_groups_layer(network, curr_layer):
    """
    Returns the amount of cultural groups considering only a layer.
    :param network: the network data.
    :param curr_layer: the layer under analysis.
    """
    return len(_cultural_groups_layer(network, curr_layer))


def get_info_cultural_groups_layer(network, curr_layer):
    """
    Returns the amount of cultural groups and the biggest one considering only a layer.
    :param network: the network data.
    :param curr_layer: the current layer being operated.
    """
    info = _cultural_groups_layer(network, curr_layer)
    return len(info), max(info.values())
