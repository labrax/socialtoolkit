#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This source defines analysis operation that are mainly related to graphs.
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
                    if population[y*height + x, i] != population[y*height + x - 1, i]:
                        isequal1 = False
                        break
            if y > 0:
                isequal2 = True
                for i in range(0, len(population[0])):
                    if population[y*height + x, i] != population[(y-1)*height + x, i]:
                        isequal2 = False
                        break
            if x > 0 and y > 0:
                isequal3 = True
                for i in range(0, len(population[0])):
                    if population[y*height + x, i] != population[(y-1)*height + x - 1, i]:
                        isequal3 = False
                        break
            if isequal1 is False and isequal2 is False and isequal3 is False:
                amount_components += 1
    return amount_components
###### MODIFIED FROM NETWORKX ######
#from nx.algorithms.components.connected
def _plain_bfs(G, source):
    """Returns the amount of nodes explored and the nodes seen from a source node using BFS.
    
    Args:
        G (networkx.classes.graph): the graph.
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
                nextlevel.update(G[v])
    return (amt, seen)
def fast_get_connected_components(G):
    """Returns a list with the sizes of each physical group.
    
    Args:
        G (networkx.classes.graph): the graph."""
    sizes = []
    seen = set()
    for v in G:
        if v not in seen:
            (amt, c) = _plain_bfs(G, v)
            bisect.insort_left(sizes, amt)
            seen.update(c)
    return sizes
def fast_get_connected_components_len(G):
    """Return the amount of physical groups.
    
    Args:
        G (networkx.classes.graph): the graph."""
    return len(fast_get_connected_components(G))
def has_path(G, node1, node2):
    """Returns True if there is a path between 2 nodes.
    
    Args:
        G (networkx.classes.graph): the graph.
        node1 (networkx.classes.nodes): the source node.
        node2 (networkx.classes.nodes): the target node."""
    try:
        nx.algorithms.shortest_paths._bidirectional_pred_succ(G, node1, node2)
        return True
    except:
        return False
###### MODIFIED FROM NETWORKX ######
