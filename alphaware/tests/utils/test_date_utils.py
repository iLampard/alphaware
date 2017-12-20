# -*- coding: utf-8 -*-

from unittest import TestCase
from parameterized import parameterized
from datetime import datetime as dt
import pandas as pd
from pandas.util.testing import assert_series_equal
from xutils.date_utils import (BizDayConventions,
                         Weekdays)
from alphaware.utils import (map_to_biz_day,
                             get_tiaocang_date)
from alphaware.enums import FreqType


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

    @parameterized.expand([('2016-01-01',
                            '2016-3-31',
                            FreqType.EOM,
                            'China.SSE',
                            '%Y-%m-%d',
                            [dt(2016, 1, 29), dt(2016, 2, 29), dt(2016, 3, 31)]),
                           ('2017-01-01',
                            '2017-02-01',
                            FreqType.EOW,
                            'China.SSE',
                            '%Y-%m-%d',
                            [dt(2017, 1, 6), dt(2017, 1, 13), dt(2017, 1, 20), dt(2017, 1, 26)]),
                           ('2016/01/01',
                            '2017/02/01',
                            FreqType.EOY,
                            'China.SSE',
                            '%Y/%m/%d',
                            [dt(2016, 12, 30)]),
                           (dt(2014, 1, 1),
                            dt(2014, 3, 31),
                            FreqType.EOM,
                            'China.SSE',
                            '%Y/%m/%d',
                            [dt(2014, 1, 30), dt(2014, 2, 28), dt(2014, 3, 31)])
                           ])
    def test_get_tiaocang_date(self, start_date, end_date, freq, calendar, date_format, expected):
        calculated = get_tiaocang_date(start_date, end_date, freq, calendar, date_format)
        self.assertEqual(calculated, expected)
