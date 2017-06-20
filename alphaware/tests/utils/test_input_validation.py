# -*- coding: utf-8 -*-

from unittest import TestCase
from parameterized import parameterized
import pandas as pd
import numpy as np
from numpy.testing.utils import assert_array_equal
from PyFin.DateUtilities import Date
from pandas.util.testing import assert_series_equal
from alphaware.utils import (ensure_pd_series,
                             ensure_pyfin_date,
                             ensure_np_array)


class TestInputValidation(TestCase):
    @parameterized.expand([([1, 2, 3], pd.Series([1, 2, 3])),
                           (np.array([1, 2, 3]), pd.Series([1, 2, 3]).astype('int32')),
                           (pd.Series([1, 2, 3]), pd.Series([1, 2, 3]))
                           ])
    def test_ensure_pd_series(self, data, expected):
        calculated = ensure_pd_series(data)
        assert_series_equal(calculated, expected)

    @parameterized.expand([('2014-01-02', '%Y-%m-%d', Date(2014, 1, 2)),
                           ('2013/05/02', '%Y/%m/%d', Date(2013, 5, 2)),
                           (Date(2013, 5, 2), '%Y/%m/%d', Date(2013, 5, 2))])
    def test_ensure_pyfin_date(self, data, date_format, expected):
        calculated = ensure_pyfin_date(data, date_format)
        self.assertEqual(calculated, expected)

    @parameterized.expand([(None, None, pd.Series([1, 2, 3]), np.array([1, 2, 3])),
                           (None, None, pd.DataFrame([[1, 2, 3], [2, 3, 4]]), np.array([[1, 2, 3], [2, 3, 4]])),
                           (None, None, np.array([1, 2, 3]), np.array([1, 2, 3]))])
    def test_ensure_np_array(self, func, argname, data, expected):
        calculated = ensure_np_array(func, argname, data)
        assert_array_equal(calculated, expected)
