# -*- coding: utf-8 -*-

from unittest import TestCase
from parameterized import parameterized
from datetime import datetime as dt
import pandas as pd
from pandas.util.testing import assert_series_equal
from PyFin.Enums import (BizDayConventions,
                         Weekdays)
from alphaware.utils import (map_to_biz_day,
                                       )


class TestDateUtils(TestCase):
    @parameterized.expand([([dt(2017, 1, 1), dt(2017, 2, 1), dt(2017, 3, 1)],
                            'China.SSE',
                            BizDayConventions.Preceding,
                            pd.Series([dt(2016, 12, 30), dt(2017, 1, 26), dt(2017, 3, 1)])),
                           ([dt(2017, 1, 1), dt(2017, 2, 1), dt(2017, 2, 1)],
                            'China.SSE',
                            BizDayConventions.Following,
                            pd.Series([dt(2017, 1, 3), dt(2017, 2, 3), dt(2017, 2, 3)]))
                           ])
    def test_map_to_biz_day(self, date_series, calendar, convention, expected):
        calculated = map_to_biz_day(date_series, calendar, convention)
        assert_series_equal(calculated, expected)
