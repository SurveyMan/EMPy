import experiman.core.rvars as rvars
import numpy as np
import operator

__add__ = "add"
__remove__ = "remove"

intern(__add__)
intern(__remove__)


def make_graph(node_list):
    """Takes a list of variables and returns a fully connected Graph object.
    :param node_list: A list of RVars indicating the nodes we should use in the graph.
    :returns: Graph object of the random variables. This is a Bayesian Network."""
    assert(all([isinstance(n, rvars.RVar) for n in node_list]))
    nodes = sorted(node_list, key=operator.attrgetter("name"))
    matrix = np.matrix([[1 for _ in range(len(node_list))] for _ in range(len(node_list))])
    # No self loops.
    for i in range(len(node_list)):
        matrix[(i, i)] = 0
    return Graph(nodes, matrix)


def update_edge(g, rv_to, rv_from, action):
    """Updates the graph to add or remove an edge.
    :param g: The graph we are updating.
    :param rv_to: The target node.
    :param rv_from: The source node.
    :param action: One of ["add", "remove"], indicating that we are adding or removing this edge.
    """
    index_to = g.nodes.index(rv_to)
    index_from = g.nodes.index(rv_from)
    if action is __add__:
        if index_from == index_to:
            raise Exception("Cannot have self edges in the graph.")
        g.matrix[(index_to, index_from)] = 1
    elif action is __remove__:
        g.matrix[(index_to, index_from)] = 0
    else:
        raise Exception("Undefined action: %s" % action)


def get_out_edges(g, rv):
    """Returns the nodes connected by out edge for the graph `g` and random variable `rv`.
    :param g: The graph we are querying.
    :param rv: The random variable whose out edges we want.
    :return: A list of random variables that are targets of the input random variable's out edges.
    """
    index = g.nodes.index(rv)
    return [rv for (i, rv) in enumerate(g.nodes) if g.matrix[index, i] == 1]


def get_in_edges(g, rv):
    """Returns the nodes connected by the edge for the graph `g` and random variable `rv`.
    :param g: The graph we querying.
    :param rv: The random variable whose in edges we want.
    :return: A list of random variables that are sources of the random variable's in edges.
    """
    index = g.nodes.index(rv)
    return [rv for (i, rv) in enumerate(g.nodes) if g.matrix[i, index] == 1]


class Graph(object):

    def __init__(self, nodes, matrix, data=None):
        self.nodes = nodes
        self.matrix = matrix
        self.data = data

    def get(self, node_name):
        for node in self.nodes:
            if node.name == node_name:
                return node