# -*- coding: utf-8 -*-

from unittest import TestCase
from parameterized import parameterized
import pandas as pd
import numpy as np
from numpy.testing.utils import assert_array_equal
from PyFin.DateUtilities import Date
from pandas.util.testing import (assert_series_equal,
                                 assert_frame_equal)
from alphaware.utils import (ensure_pd_series,
                             ensure_pyfin_date,
                             ensure_np_array,
                             ensure_pd_index_names)
from alphaware.enums import OutputDataFormat
from alphaware.const import (INDEX_FACTOR,
                             INDEX_INDUSTRY_WEIGHT)


class TestInputValidation(TestCase):
    @parameterized.expand([([1, 2, 3], pd.Series([1, 2, 3])),
                           (np.array([1.0, 2.0, 3.0]), pd.Series([1.0, 2.0, 3.0])),
                           (pd.Series([1, 2, 3]), pd.Series([1, 2, 3]))
                           ])
    def test_ensure_pd_series(self, data, expected):
        calculated = ensure_pd_series(None, None, data)
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

    @parameterized.expand([(pd.DataFrame([1, 2],
                                         index=pd.MultiIndex.from_product([['2010-01-01', '2010-01-02'], ['001']],
                                                                          names=['trade_date', 'sec'])),
                            OutputDataFormat.MULTI_INDEX_DF,
                            INDEX_INDUSTRY_WEIGHT,
                            pd.DataFrame([1, 2],
                                         index=pd.MultiIndex.from_product([['2010-01-01', '2010-01-02'], ['001']],
                                                                          names=['trade_date', 'industry_code'])
                                         )),
                           (pd.DataFrame([1, 2], index=pd.Index(['2010-01-01', '2010-01-02'], name='trade_date')),
                            OutputDataFormat.PITVOT_TABLE_DF,
                            INDEX_FACTOR,
                            pd.DataFrame([1, 2], index=pd.Index(['2010-01-01', '2010-01-02'], name='trade_date'))
                            )])
    def test_ensure_pd_index_names(self, data, data_format, valid_index, expected):
        calculated = ensure_pd_index_names(data, data_format, valid_index)
        assert_frame_equal(calculated, expected)
