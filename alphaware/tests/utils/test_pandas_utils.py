# -*- coding: utf-8 -*-

from unittest import TestCase
from parameterized import parameterized
import pandas as pd
from pandas import (MultiIndex,
                    Index)
from pandas.util.testing import assert_frame_equal
from alphaware.enums import OutputDataFormat
from alphaware.const import INDEX_FACTOR
from alphaware.utils import convert_df_format, top


class TestPandasUtils(TestCase):
    @parameterized.expand([(pd.DataFrame({'001': [1, 2, 3], '002': [2, 3, 4]}, index=['2014', '2015', '2016']),
                            OutputDataFormat.MULTI_INDEX_DF,
                            'test_factor',
                            INDEX_FACTOR,
                            pd.DataFrame(index=MultiIndex(levels=[['2014', '2015', '2016'], ['001', '002']],
                                                          labels=[[0, 0, 1, 1, 2, 2], [0, 1, 0, 1, 0, 1]],
                                                          names=['tradeDate', 'secID']),
                                         data=[1, 2, 2, 3, 3, 4],
                                         columns=['test_factor']))])
    def test_convert_df_format_1(self, data, target_format, col_name, multi_index, expected):
        calculated = convert_df_format(data, target_format, col_name, multi_index)
        assert_frame_equal(calculated, expected)

    @parameterized.expand(
        [(pd.DataFrame(
            index=MultiIndex.from_product([['2014', '2015', '2016'], ['001', '002']], names=['tradeDate', 'secID']),
            data=[1, 2, 3, 4, 5, 6],
            columns=['factor']),
          OutputDataFormat.PITVOT_TABLE_DF,
          'factor',
          INDEX_FACTOR,
          pd.DataFrame({'001': [1, 3, 5], '002': [2, 4, 6]},
                       index=Index(['2014', '2015', '2016'], name='tradeDate')))])
    def test_convert_df_format_2(self, data, target_format, col_name, multi_index, expected):
        calculated = convert_df_format(data, target_format, col_name, multi_index)
        assert_frame_equal(calculated, expected)

    @parameterized.expand(
        [(pd.DataFrame(data=[1, 2, 3, 4, 5, 6, 7, 8], columns=['1']),
          pd.DataFrame(data=[8, 7, 6, 5, 4], index=[7, 6, 5, 4, 3], columns=['1'])
          )])
    def test_top(self, data, expected):
        calculated = top(data, column=['1'])
        assert_frame_equal(calculated, expected)
