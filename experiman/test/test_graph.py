import experiman.core.rvars as rvars
import experiman.qc.utils as utils
import numpy
import operator
import StringIO
import unittest
import urllib2

smoking = urllib2.urlopen("http://data.princeton.edu/wws509/datasets/smoking.dat").read()
smoking_data = numpy.loadtxt(StringIO.StringIO(smoking),
                             dtype={"names": ("row", "age", "smoke", "pop", "dead"),
                                    "formats": (numpy.int8, "S5", "S20", numpy.int16, numpy.int16)},
                             skiprows=1
                             )
smoking_data_headers = smoking_data.dtype.fields.keys()


class RVarsTest(unittest.TestCase):

    def setUp(self):
        rvars.RVar.reset()

    def test_rvar_initialization(self):
        for v in smoking_data_headers:
            rvars.RVar(v)
        self.assertEqual(len(smoking_data_headers), len(rvars.RVar.all_random_variables.keys()))
        for v in smoking_data_headers:
            rvars.RVar(v)
        self.assertEqual(len(smoking_data_headers), len(rvars.RVar.all_random_variables.keys()))

    def test_make_graph(self):
        node_list = []
        for v in smoking_data_headers:
            node_list.append(rvars.RVar(v))
        g = utils.make_graph(node_list)
        self.assertListEqual(sorted(node_list, key=operator.attrgetter("name")), g.nodes)
        for i in range(len(node_list)):
            for j in range(len(node_list)):
                if i == j:
                    self.assertEquals(g.matrix[(i, j)], 0)
                else:
                    self.assertEquals(g.matrix[(i, j)], 1)

    def test_update_edge(self):
        node_list = []
        for v in smoking_data_headers:
            node_list.append(rvars.RVar(v))
        g = utils.make_graph(node_list)
        # Test adding a self edge.
        self.assertRaises(Exception, utils.update_edge(g, node_list[0], node_list[0], action="add"))
        # Test removing an edge
        utils.update_edge(g, node_list[0], node_list[1], action="remove")
        self.assertEqual(g.matrix[(0, 1)], 0)
        # Test adding back that edge
        utils.update_edge(g, node_list[0], node_list[1], action="add")
        self.assertEqual(g.matrix[(0, 1)], 1)
        self.assertRaises(Exception, utils.update_edge(g, node_list[0], node_list[1], action="update"))

    def test_get_edges(self):
        node_list = []
        for v in smoking_data_headers:
            node_list.append(rvars.RVar(v))
        g = utils.make_graph(node_list)
        # Test get out edges
        rvs = utils.get_out_edges(g, node_list[0])
        self.assertListEqual(sorted(rvs), sorted([n for n in node_list if not n == node_list[0]]))
        utils.update_edge(g, node_list[0], node_list[1], action="remove")
        rvs = utils.get_out_edges(g, node_list[0])
        self.assertListEqual(sorted(rvs), sorted([n for n in node_list if not (n == node_list[0] or n == node_list[1])]))
        # Test get in edges
        rvs = utils.get_in_edges(g, node_list[0])
        self.assertListEqual(sorted(rvs), sorted([n for n in node_list if not n == node_list[0]]))
        utils.update_edge(g, node_list[1], node_list[0], action="remove")
        rvs = utils.get_in_edges(g, node_list[0])
        self.assertListEqual(sorted(rvs), sorted([n for n in node_list if not (n == node_list[0] or n == node_list[1])]))