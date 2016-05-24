
import unittest

from stk import STK
from paper_axelrod1997 import run as axelrodrun
from paper_future_multilayer import run as multilayerrun
from socialtoolkit.worker import work


class STKtests(unittest.TestCase):
    def test_default(self):
        try:
            a = STK()
            a.run()
        except Exception as e:
            self.fail("STK raised Exception" + e)


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
