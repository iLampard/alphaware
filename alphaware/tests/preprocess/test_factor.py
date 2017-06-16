# -*- coding: utf-8 -*-

from unittest import TestCase
import pandas as pd
from pandas.util.testing import assert_frame_equal
from datetime import datetime as dt
from ...preprocess import Factor
from ...enums import (FactorType,
                      OutputDataFormat)


class TestFactor(TestCase):
    def test_factor_1(self):
        index = pd.MultiIndex.from_product([['2014-01-30', '2014-02-28', '2014-03-31'], ['001', '002']],
                                           names=['tradeDate', 'secID'])
        data = pd.DataFrame(index=index, data=[1, 2, 3, 4, 5, 6])
        factor = Factor(data=data, name='test', production_data_format=OutputDataFormat.PITVOT_TABLE_DF)

        self.assertEqual(factor.factor_type, FactorType.ALPHA_FACTOR)
        self.assertEqual(factor.trade_date_list, [dt(2014, 1, 30), dt(2014, 2, 28), dt(2014, 3, 31)])

        factor_data_expected = pd.DataFrame({'001': [1, 3, 5], '002': [2, 4, 6]},
                                            index=pd.Index([dt(2014, 1, 30), dt(2014, 2, 28), dt(2014, 3, 31)],
                                                           name='tradeDate'))
        assert_frame_equal(factor.factor_data, factor_data_expected)

    def test_factor_2(self):
        data = pd.DataFrame({'001': [1, 3, 5], '002': [2, 4, 6]},
                            index=pd.Index([dt(2014, 1, 30), dt(2014, 2, 28), dt(2014, 3, 31)],
                                           name='tradeDate'))
        property_dict = {'data_format': OutputDataFormat.PITVOT_TABLE_DF}
        factor = Factor(data=data,
                        name='test',
                        property_dict=property_dict,
                        production_data_format=OutputDataFormat.MULTI_INDEX_DF)

        self.assertEqual(factor.factor_type, FactorType.ALPHA_FACTOR)
        self.assertEqual(factor.trade_date_list, [dt(2014, 1, 30), dt(2014, 2, 28), dt(2014, 3, 31)])

        index = pd.MultiIndex.from_product([[dt(2014, 1, 30), dt(2014, 2, 28), dt(2014, 3, 31)], ['001', '002']],
                                           names=['tradeDate', 'secID'])
        factor_data_expected = pd.DataFrame(index=index, data=[1, 2, 3, 4, 5, 6], columns=['test'])
        assert_frame_equal(factor.factor_data, factor_data_expected)
