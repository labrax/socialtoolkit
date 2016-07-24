#!/usr/bin/python

from stk import STK
from paper_axelrod1997 import run as axelrodrun
from paper_future_multilayer import run as multilayerrun
from socialtoolkit.worker import work
from socialtoolkit.errors.parameter_error import ParameterError
import unittest
import sys


class STKtests(unittest.TestCase):
    def test_executions(self):
        algorithms = ['axelrod', 'centola', 'klemm']
        for a in algorithms:
            try:
                sys.argv = ['./stk.py', '-gs', '5', '-f', '2', '-t', '2', '-cI', '150000', '-A', a, '-l', '2']
                a = STK()
                a.run()
            except Exception as e:
                self.fail("STK raised Exception" + e)

    def test_invalid_algorithm(self):
        sys.argv = ['./stk.py', '-gs', '5', '-f', '2', '-t', '2', '-cI', '150000', '-A', 'invalid']
        self.assertRaises(ParameterError, lambda: STK())

    def test_negative_step_analysis(self):
        sys.argv = ['./stk.py', '-gs', '5', '-f', '2', '-t', '2', '-cI', '150000', '-SA', '-1']
        self.assertRaises(ParameterError, lambda: STK())

    def test_negative_gridsize(self):
        sys.argv = ['./stk.py', '-gs', '-5', '-f', '2', '-t', '2', '-cI', '150000', '-SA', '50']
        self.assertRaisesRegexp(ParameterError, "gridsize", lambda: STK())

    def test_no_parameter(self):
        sys.argv = ['./stk.py', '-f', '2', '-l', '3']
        self.assertRaisesRegexp(ParameterError, "Invalid", lambda: STK())


class CulturalGroupsTopology(unittest.TestCase):
    def test_relation_1_2_1(self):
        from socialtoolkit.graph.network import Network, graph_from_file, population_from_file
        from socialtoolkit.algorithm.analysis.cultural_groups import get_info_cultural_groups_topology
        network = Network(graph_from_file("examples_and_tests/graph_cultural_groups_topology.el"),
                          population_from_file("examples_and_tests/graph_cultural_groups_topology.pd"), 1)
        self.assertEqual(get_info_cultural_groups_topology(network.graph, network.population_data), [(1, (0.0,)), (1, (0.0,)), (2, (1.0,))])

    def test_relation_1_2_1_2features(self):
        from socialtoolkit.graph.network import Network, graph_from_file, population_from_file
        from socialtoolkit.algorithm.analysis.cultural_groups import get_info_cultural_groups_topology
        network = Network(graph_from_file("examples_and_tests/graph_cultural_groups_topology.el"),
                          population_from_file("examples_and_tests/graph_cultural_groups_topology_2features.pd"), 1)
        self.assertEqual(get_info_cultural_groups_topology(network.graph, network.population_data),
                         [(1, (0.0, 0.0)), (1, (0.0, 0.0)), (2, (1.0, 0.0))])

    def test_relation_4(self):
        from socialtoolkit.graph.network import Network, graph_from_file, population_from_file
        from socialtoolkit.algorithm.analysis.cultural_groups import get_info_cultural_groups_topology
        network = Network(graph_from_file("examples_and_tests/graph_cultural_groups_topology.el"),
                          population_from_file("examples_and_tests/graph_cultural_groups_topology_equal.pd"), 1)
        self.assertEqual(get_info_cultural_groups_topology(network.graph, network.population_data), [(4, (1.0,))])


class PaperTests(unittest.TestCase):
    def test_paper_axelrod(self):
        try:
            self.assertGreater(axelrodrun(), 10001)
        except Exception as e:
            self.fail("Axelrod's run raised Exception" + e)

    def test_paper_multilayer(self):
        try:
            multilayerrun()
        except Exception as e:
            self.fail("Multilayers's run raised Exception" + e)

if __name__ == "__main__":
    unittest.main()
