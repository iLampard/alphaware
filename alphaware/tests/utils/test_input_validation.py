# -*- coding: utf-8 -*-

from unittest import TestCase
from parameterized import parameterized
from datetime import datetime as dt
import pandas as pd
from PyFin.DateUtilities import Date
from pandas.util.testing import assert_series_equal
from alphaware.utils import (ensure_pd_series,
                             ensure_pyfin_date)


class TestInputValidation(TestCase):
    @parameterized.expand([([1, 2, 3], pd.Series([1, 2, 3]))
                           ])
    def test_ensure_pd_series(self, data, expected):
        calculated = ensure_pd_series(data)
        assert_series_equal(calculated, expected)

    @parameterized.expand([('2014-01-02', '%Y-%m-%d', Date(2014, 1, 2))
                           ])
    def test_ensure_pyfin_date(self, data, expected):
        calculated = ensure_pyfin_date(data)
        assert_series_equal(calculated, expected)
