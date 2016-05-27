# -*- coding: utf-8 -*-

"""
This source defines analysis related to physical groups.
"""

import networkx as nx
from math import sqrt
import bisect


def get_grid_groups_axelrod(G, population):
    """Returns the amount of cultural groups for a grid in relation to its neighbors.

    Args:
        G (networkx.classes.graph): the graph.
        population (list of list): the features and traits of the population."""
    height = width = int(sqrt(len(nx.nodes(G))))

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
    """Returns the amount of nodes explored and the nodes seen from a source node using BFS.

    Args:
        graph (networkx.classes.graph): the graph.
        source (networkx.classes.nodes): the source node."""
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


def fast_get_connected_components(graph):
    """Returns a list with the sizes of each physical group.

    Args:
        graph (networkx.classes.graph): the graph."""
    sizes = list()
    seen = set()
    for v in graph:
        if v not in seen:
            (amt, c) = _plain_bfs(graph, v)
            bisect.insort_left(sizes, amt)
            seen.update(c)
    return sizes


def has_path(graph, node1, node2):
    """Returns True if there is a path between 2 nodes.

    Args:
        graph (networkx.classes.graph): the graph.
        node1 (networkx.classes.nodes): the source node.
        node2 (networkx.classes.nodes): the target node."""
    try:
        nx.algorithms.shortest_paths._bidirectional_pred_succ(graph, node1, node2)
        return True
    except:
        return False


def get_amount_physical_groups(graph):
    """Returns the amount of physical groups.

    Args:
        graph (networkx.classes.graph): the graph."""
    return len(fast_get_connected_components(graph))


def get_size_biggest_physical_groups(graph):
    """Returns the size of the biggest physical group.

    Args:
        graph (networkx.classes.graph): the graph."""
    return max(fast_get_connected_components(graph))


def get_info_physical_groups(graph):
    """Returns the amount of physical groups and the biggest one.

    Args:
        graph (networkx.classes.graph): the graph list."""
    info = fast_get_connected_components(graph)
    return len(info), max(info)


def get_amount_physical_groups_unify(graph):
    """Returns the amount of physical groups unifying layers.

    Args:
        graph (list of networkx.classes.graph): the graph list."""
    new_graph = nx.compose_all(graph)
    return len(fast_get_connected_components(new_graph))


def get_size_biggest_physical_groups_unify(graph):
    """Returns the size of the biggest physical group unifying layers.

    Args:
        graph (list of networkx.classes.graph): the graph list."""
    new_graph = nx.compose_all(graph)
    return max(fast_get_connected_components(new_graph))


def get_info_physical_groups_unify(graph):
    """Returns the amount of physical groups and the biggest one unifying layers.

    Args:
        graph (list of networkx.classes.graph): the graph list."""
    new_graph = nx.compose_all(graph)
    info = fast_get_connected_components(new_graph)
    return len(info), max(info)
