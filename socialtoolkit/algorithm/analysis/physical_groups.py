# -*- coding: utf-8 -*-

"""
This source defines analysis related to physical groups.
"""

import networkx as nx
from math import sqrt
import bisect

from socialtoolkit.graph import Network


def get_grid_groups_axelrod(network, curr_layer=0):
    """
    Returns the amount of cultural groups for a grid in relation to its neighbors.
    :param network: the network data.
    :param curr_layer: the layer under analysis.
    """
    height = width = int(sqrt(len(nx.nodes(network.graph[curr_layer]))))
    population = network.population_data

    amount_components = 0
    for y in range(0, height):
        for x in range(0, width):
            isequal1 = isequal2 = isequal3 = False
            if x > 0:
                isequal1 = True
                for i in range(0, len(population[0])):
                    if population[y * height + x, i] != population[y * height + x - 1, i]:
                        isequal1 = False
                        break
            if y > 0:
                isequal2 = True
                for i in range(0, len(population[0])):
                    if population[y * height + x, i] != population[(y - 1) * height + x, i]:
                        isequal2 = False
                        break
            if x > 0 and y > 0:
                isequal3 = True
                for i in range(0, len(population[0])):
                    if population[y * height + x, i] != population[(y - 1) * height + x - 1, i]:
                        isequal3 = False
                        break
            if isequal1 is False and isequal2 is False and isequal3 is False:
                amount_components += 1
    return amount_components


"""The following are codes modified from networkx.algorithms.components.connected"""


def _plain_bfs(graph, source):
    """
    Returns the amount of nodes explored and the nodes seen from a source node using BFS.
    :param graph (networkx.classes.graph): the graph.
    :param source (networkx.classes.nodes): the source node.
    """
    seen = set()
    amt = 0
    nextlevel = {source}
    while nextlevel:
        thislevel = nextlevel
        nextlevel = set()
        for v in thislevel:
            if v not in seen:
                seen.add(v)
                amt += 1
                nextlevel.update(graph[v])
    return amt, seen


def fast_get_connected_components(network, curr_layer=0):
    """
    Returns a list with the sizes of each physical group.
    :param network: the network data.
    :param curr_layer: the layer under analysis.
    """
    sizes = list()
    seen = set()
    for v in network.graph[curr_layer]:
        if v not in seen:
            (amt, c) = _plain_bfs(network.graph[curr_layer], v)
            bisect.insort_left(sizes, amt)
            seen.update(c)
    return sizes


def has_path(network, node1, node2, curr_layer=0):
    """
    Returns True if there is a path between 2 nodes.
    :param network: the network data.
    :param node1 (networkx.classes.nodes): the source node.
    :param node2 (networkx.classes.nodes): the target node.
    :param curr_layer: the layer under analysis.
    """
    try:
        nx.algorithms.shortest_paths._bidirectional_pred_succ(network.graph[curr_layer], node1, node2)
        return True
    except:
        return False


def get_amount_physical_groups(network, curr_layer=0):
    """
    Returns the amount of physical groups.
    :param network: the network data.
    :param curr_layer: the layer under analysis.
    """
    return len(fast_get_connected_components(network, curr_layer))


def get_size_biggest_physical_groups(network, curr_layer=0):
    """
    Returns the size of the biggest physical group.
    :param network: the network data.
    :param curr_layer: the layer under analysis.
    """
    return max(fast_get_connected_components(network, curr_layer))


def get_info_physical_groups(network, curr_layer=0):
    """
    Returns the amount of physical groups and the biggest one.
    :param network: the network data.
    :param curr_layer: the layer under analysis.
    """
    info = fast_get_connected_components(network, curr_layer)
    return len(info), max(info)


def get_amount_physical_groups_unify(network):
    """
    Returns the amount of physical groups unifying layers.
    :param network: the network data.
    """
    new_network = Network(nx.compose_all(network.graph), list(), 0)
    return len(fast_get_connected_components(new_network))


def get_size_biggest_physical_groups_unify(network):
    """
    Returns the size of the biggest physical group unifying layers.
    :param network: the network data.
    """
    new_network = Network(nx.compose_all(network.graph), list(), 0)
    return max(fast_get_connected_components(new_network))


def get_info_physical_groups_unify(network):
    """
    Returns the amount of physical groups and the biggest one unifying layers.
    :param network: the network data.
    """
    new_network = Network(nx.compose_all(network.graph), list(), 0)
    info = fast_get_connected_components(new_network)
    return len(info), max(info)
