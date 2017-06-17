# -*- coding: utf-8 -*-

from unittest import TestCase
import pandas as pd
import numpy as np
from numpy.testing import assert_array_equal
from alphaware.preprocess import ExtCategoricalImputer
from alphaware.enums import NAStrategy


class TestExtCategoricalImputer(TestCase):
    def test_default(self):
        calculated = ExtCategoricalImputer().fit_transform(np.array(['a', 'b', 'b', None, 'c']))
        expected = np.array(['a', 'b', 'b', 'b', 'c'], dtype=object)
        assert_array_equal(calculated, expected)

        calculated = ExtCategoricalImputer().fit_transform(pd.Series(['a', 'b', 'b', np.nan, 'c']))
        expected = np.array(['a', 'b', 'b', 'b', 'c'], dtype=object)
        assert_array_equal(calculated, expected)

    def test_ext(self):
        calculated = ExtCategoricalImputer(strategy=NAStrategy.CUSTOM, custom_value='d') \
            .fit_transform(np.array(['a', 'b', 'b', None, 'c', 'd']))
        expected = np.array(['a', 'b', 'b', 'd', 'c', 'd'], dtype=object)
        assert_array_equal(calculated, expected)

        calculated = ExtCategoricalImputer(strategy=NAStrategy.CUSTOM, custom_value='x') \
            .fit_transform(pd.Series(['a', 'b', 'b', np.nan, 'c', 'd']))
        expected = np.array(['a', 'b', 'b', 'x', 'c', 'd'], dtype=object)
        assert_array_equal(calculated, expected)
