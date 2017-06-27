# -*- coding: utf-8 -*-

from unittest import TestCase
from parameterized import parameterized
import pandas as pd
from pandas.util.testing import assert_frame_equal
from numpy.testing import assert_array_equal
from alphaware.selector import BrutalSelector
from alphaware.enums import SelectionMethod


class TestSelector(TestCase):
    @parameterized.expand(
        [(pd.Series([3, 2, 4, 5, 6], index=['001', '002', '003', '004', '005']),
          2,
          0.1,
          pd.DataFrame([50.0, 50.0], index=['005', '004'], columns=['weight'])),
         (pd.Series([3, 2, 4, -5, -6], index=['001', '002', '003', '004', '005']),
          2,
          0.1,
          pd.DataFrame([50.0, 50.0], index=['003', '001'], columns=['weight'])),
         (pd.Series([3, 2, 4, 5, 6], index=['001', '002', '003', '004', '005']),
          None,
          0.8,
          pd.DataFrame([25.0, 25.0, 25.0, 25.0], index=['005', '004', '003', '001'], columns=['weight']))])
    def test_brutal_selector(self, X, nb_select, prop_select, expected):
        calculated = BrutalSelector(nb_select, prop_select).fit_transform(X)
        assert_frame_equal(calculated, expected)
