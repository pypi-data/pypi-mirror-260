import unittest
import os
from ..src.labneura.eda.profiler import Profiler


class TestProfiler(unittest.TestCase):
    def setUp(self) -> None:
        self.df_path = os.path.join(os.path.dirname(
            __file__), "assets", "titanic.csv")

    def test_1(self):
        p = Profiler(self.df_path)
        p.profile()

    def test_2(self):
        with self.assertRaises(ValueError):
            p = Profiler(123)

    def test_3(self):
        with self.assertRaises(ValueError):
            p = Profiler("titanic.txt")
    
    def test_4(self):
        with self.assertRaises(ValueError):
            p = Profiler("titanic.csv")

    def test_5(self):
        with self.assertRaises(ValueError):
            p = Profiler()
            p.df_path = None
            p.profile()
        