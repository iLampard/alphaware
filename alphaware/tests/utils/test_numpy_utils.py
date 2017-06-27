# -*- coding: utf-8 -*-

from unittest import TestCase
from parameterized import parameterized
import numpy as np
from numpy.testing import assert_array_equal
from alphaware.utils import (index_n_largest,
                             index_n_smallest)


class TestNumpyUtils(TestCase):
    @parameterized.expand([(np.array([1, 2, 5, -1]), 2, np.array([2, 1])),
                           (np.array([7, 2, 5, -1]), 3, np.array([0, 2, 1]))])
    def test_index_n_largest(self, array, n, expected):
        calculated = index_n_largest(array, n)
        assert_array_equal(calculated, expected)

    @parameterized.expand([(np.array([1, 2, 5, -1]), 2, np.array([3, 0])),
                           (np.array([7, 2, 5, -1]), 3, np.array([3, 1, 2]))])
    def test_index_n_largest(self, array, n, expected):
        calculated = index_n_smallest(array, n)
        assert_array_equal(calculated, expected)
