import unittest

import numpy as np

from assembly import Assembly


class TestAssembly(unittest.TestCase):

    def test_init(self):
        ass = Assembly()
        labels = ass.coalesce(np.array([[0., 0.], [2., 2.]]))
        self.assertTrue(np.array_equal(labels, [0, 1]))

    def test_reverse(self):
        ass = Assembly()
        ass.coalesce(np.array([[0., 0.], [2., 2.]]))
        labels = ass.coalesce(np.array([[1.9, 1.9], [0.1, 0.1]]))
        self.assertTrue(np.array_equal(labels, [1, 0]))
        self.assertTrue(np.array_equal(ass.points, [[0.1, 0.1], [1.9, 1.9]]))

    def test_longer(self):
        ass = Assembly()
        ass.coalesce(np.array([[0., 0.], [2., 2.]]))
        labels = ass.coalesce(np.array([[1.9, 1.9], [3., 3.], [0.1, 0.1]]))
        self.assertTrue(np.array_equal(labels, [1, 2, 0]))
        self.assertTrue(np.array_equal(ass.points, [[0.1, 0.1], [1.9, 1.9], [3., 3.]]))

    def test_shorter(self):
        ass = Assembly()
        ass.coalesce(np.array([[0., 0.], [2., 2.]]))
        labels = ass.coalesce(np.array([[1.9, 1.9]]))
        self.assertTrue(np.array_equal(labels, [1]))
        self.assertTrue(np.array_equal(ass.points, [[0., 0.], [1.9, 1.9]]))

    def test_coalesce(self):
        ass = Assembly()
        ass.coalesce(np.array([[0., 0.], [2., 2.]]))
        ass.coalesce(np.array([[1.9, 1.9], [3, 3], [0.1, 0.1]]))
        labels = ass.coalesce(np.array([[2.9, 2.9], [2.1, 2.1]]))
        self.assertTrue(np.array_equal(labels, [2, 1]))
        self.assertTrue(np.array_equal(ass.points, [[0.1, 0.1], [2.1, 2.1], [2.9, 2.9]]))

