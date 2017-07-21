# -*- coding: utf-8 -*-

from unittest import TestCase
from parameterized import parameterized
import pandas as pd
import numpy as np
from numpy.testing.utils import assert_array_equal
from pandas import (MultiIndex,
                    Index)
from pandas.util.testing import assert_frame_equal, assert_series_equal
from alphaware.enums import OutputDataFormat, FreqType
from alphaware.const import INDEX_FACTOR
from alphaware.utils import (convert_df_format,
                             top,
                             group_by_freq,
                             fwd_return,
                             weighted_rank)
from datetime import datetime as dt


class TestPandasUtils(TestCase):
    @parameterized.expand([(pd.DataFrame({'001': [1, 2, 3], '002': [2, 3, 4]}, index=['2014', '2015', '2016']),
                            OutputDataFormat.MULTI_INDEX_DF,
                            'test_factor',
                            INDEX_FACTOR,
                            pd.DataFrame(index=MultiIndex(levels=[['2014', '2015', '2016'], ['001', '002']],
                                                          labels=[[0, 0, 1, 1, 2, 2], [0, 1, 0, 1, 0, 1]],
                                                          names=['date', 'secID']),
                                         data=[1, 2, 2, 3, 3, 4],
                                         columns=['test_factor']))])
    def test_convert_df_format_1(self, data, target_format, col_name, multi_index, expected):
        calculated = convert_df_format(data, target_format, col_name, multi_index)
        assert_frame_equal(calculated, expected)

    @parameterized.expand(
        [(pd.DataFrame(
            index=MultiIndex.from_product([['2014', '2015', '2016'], ['001', '002']], names=['date', 'secID']),
            data=[1, 2, 3, 4, 5, 6],
            columns=['factor']),
          OutputDataFormat.PITVOT_TABLE_DF,
          'factor',
          INDEX_FACTOR,
          pd.DataFrame({'001': [1, 3, 5], '002': [2, 4, 6]},
                       index=Index(['2014', '2015', '2016'], name='date')))])
    def test_convert_df_format_2(self, data, target_format, col_name, multi_index, expected):
        calculated = convert_df_format(data, target_format, col_name, multi_index)
        assert_frame_equal(calculated, expected)

    @parameterized.expand(
        [(pd.DataFrame(data=[[1, 23, 4, 5], [4, 5, 7, 8], [10, 5, 11, 8], [34, 65, 27, 78]],
                       columns=['A', 'B', 'C', 'D']),
          2,
          ['A'],
          pd.DataFrame(data=[[34, 65, 27, 78], [10, 5, 11, 8]], index=[3, 2], columns=['A', 'B', 'C', 'D'])
          )])
    def test_top_1(self, data, n, column, expected):
        calculated = top(data, column=column, n=n)
        assert_frame_equal(calculated, expected)

    @parameterized.expand(
        [(pd.Series(data=[35, 12, 45, 79, 123, 74, 35]),
          3,
          pd.Series(data=[123, 79, 74], index=[4, 3, 5])
          )])
    def test_top_2(self, data, n, expected):
        calculated = top(data, n=n)
        assert_series_equal(calculated, expected)

    @parameterized.expand(
        [(pd.DataFrame(data=[1, 2, 3, 4, 5, 6, 7, 9, 0, 12],
                       index=[dt(2017, 7, 1), dt(2017, 6, 1), dt(2017, 7, 2), dt(2017, 6, 1), dt(2017, 3, 1),
                              dt(2017, 3, 1), dt(2017, 1, 1), dt(2017, 2, 1), dt(2017, 1, 1), dt(2017, 2, 1)]),
          dt(2017, 7, 31),
          FreqType.EOM,
          pd.DataFrame(data=[1, 3], index=[dt(2017, 7, 1), dt(2017, 7, 2)])
          ),
         (pd.Series(data=[1, 2, 3, 4, 5, 6, 7, 9, 0, 12],
                    index=[dt(2016, 7, 1), dt(2016, 6, 1), dt(2017, 7, 2), dt(2017, 7, 1), dt(2017, 3, 1),
                           dt(2017, 3, 1), dt(2017, 1, 1), dt(2017, 2, 1), dt(2017, 1, 1), dt(2017, 2, 1)]),
          dt(2016, 12, 31),
          FreqType.EOY,
          pd.DataFrame(data=[2, 1], index=[dt(2016, 6, 1), dt(2016, 7, 1)])
          ),
         (pd.Series(data=[1, 2, 3, 4, 5, 6, 7, 9, 0, 12],
                    index=[dt(2016, 7, 1), dt(2016, 7, 1), dt(2017, 7, 2), dt(2017, 7, 1), dt(2017, 3, 1),
                           dt(2017, 3, 1), dt(2017, 1, 1), dt(2017, 2, 1), dt(2017, 1, 1), dt(2017, 2, 1)]),
          (2016, 7, 1),
          FreqType.EOD,
          pd.DataFrame(data=[1, 2], index=[dt(2016, 7, 1), dt(2016, 7, 1)])
          )
         ])
    def test_group_by_freq(self, data, group, freq, expected):
        calculated = group_by_freq(data, freq=freq).get_group(group)
        assert_frame_equal(calculated, expected)

    @parameterized.expand([(pd.Series(data=[1, 2, 3, 4],
                                      index=pd.MultiIndex.from_product([[dt(2014, 1, 30), dt(2014, 2, 28)], ['a', 'b']],
                                                                       names=['date', 'secID'])),
                            1,
                            pd.DataFrame(data=[3, 4],
                                         index=pd.MultiIndex.from_product([[dt(2014, 1, 30)], ['a', 'b']],
                                                                          names=['date', 'secID']),
                                         columns=['fwd_return'])
                            ),
                           (pd.DataFrame(data=[1, 2, 3, 4, 5, 6],
                                         index=pd.MultiIndex.from_product(
                                             [[dt(2014, 1, 30), dt(2014, 2, 28), dt(2014, 3, 30)], ['a', 'b']],
                                             names=['date', 'secID'])),
                            2,
                            pd.DataFrame(data=[5, 6],
                                         index=pd.MultiIndex.from_product([[dt(2014, 1, 30)], ['a', 'b']],
                                                                          names=['date', 'secID']),
                                         columns=['fwd_return'])
                            )
                           ])
    def test_fwd_return(self, data, period, expected):
        calculated = fwd_return(data, period=period)
        assert_frame_equal(calculated, expected)

    @parameterized.expand(
        [(pd.DataFrame({'a': [1, 2, 3], 'b': [2, 4, 6]}), [1, 1], None, True, pd.DataFrame([0.0, 1.0, 2.0])),
         (pd.DataFrame({'a': [1, 2, 3], 'b': [2, 4, 6]}), [1, 0], [0.6, 0.4], False, np.array([0.8, 1.0, 1.2]))])
    def test_weighted_rank(self, data, order, weight, out_df, expected):
        calculated = weighted_rank(data, order, weight, out_df)
        if isinstance(expected, pd.DataFrame):
            assert_frame_equal(calculated, expected)
        else:
            assert_array_equal(calculated, expected)
