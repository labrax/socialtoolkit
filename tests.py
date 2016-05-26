#!/usr/bin/python

import unittest

from stk import STK
from paper_axelrod1997 import run as axelrodrun
from paper_future_multilayer import run as multilayerrun
from socialtoolkit.worker import work
import sys
from socialtoolkit.errors.parameter_error import ParameterError

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


class PaperTests(unittest.TestCase):
    def test_paper_axelrod(self):
        try:
            axelrodrun()
        except Exception as e:
            self.fail("Axelrod's run raised Exception" + e)

    def test_paper_multilayer(self):
        try:
            multilayerrun()
        except Exception as e:
            self.fail("Multilayers's run raised Exception" + e)

if __name__ == "__main__":
    unittest.main()
