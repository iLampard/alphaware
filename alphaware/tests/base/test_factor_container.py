# -*- coding: utf-8 -*-

from unittest import TestCase
import pandas as pd
import numpy as np
from pandas.util.testing import assert_frame_equal
from datetime import datetime as dt
from alphaware.base import (Factor,
                            FactorContainer)
from alphaware.enums import (FactorType,
                             OutputDataFormat,
                             FreqType,
                             FactorNormType)


class TestFactorContainer(TestCase):
    def test_factor_1(self):
        index = pd.MultiIndex.from_product([['2014-01-30', '2014-02-28', '2014-03-31'], ['001', '002']],
                                           names=['tradeDate', 'secID'])
        data = pd.DataFrame(index=index, data=[1, 2, 3, 4, 5, 6])
        factor = Factor(data=data, name='test', production_data_format=OutputDataFormat.PITVOT_TABLE_DF)

        self.assertEqual(factor.type, FactorType.ALPHA_FACTOR)
        self.assertEqual(factor.trade_date_list, [dt(2014, 1, 30), dt(2014, 2, 28), dt(2014, 3, 31)])
        self.assertEqual(factor.production_data_format, OutputDataFormat.PITVOT_TABLE_DF)
        self.assertEqual(factor.freq, FreqType.EOM)

        factor_data_expected = pd.DataFrame({'001': [1, 3, 5], '002': [2, 4, 6]},
                                            index=pd.Index([dt(2014, 1, 30), dt(2014, 2, 28), dt(2014, 3, 31)],
                                                           name='tradeDate'))
        assert_frame_equal(factor.data, factor_data_expected)

    def test_factor_2(self):
        data = pd.DataFrame({'001': [1, 3, 5], '002': [2, 4, 6]},
                            index=pd.Index([dt(2014, 1, 30), dt(2014, 2, 28), dt(2014, 3, 31)],
                                           name='tradeDate'))
        property_dict = {'data_format': OutputDataFormat.PITVOT_TABLE_DF}
        factor = Factor(data=data,
                        name='test',
                        property_dict=property_dict,
                        production_data_format=OutputDataFormat.MULTI_INDEX_DF)

        self.assertEqual(factor.type, FactorType.ALPHA_FACTOR)
        self.assertEqual(factor.trade_date_list, [dt(2014, 1, 30), dt(2014, 2, 28), dt(2014, 3, 31)])
        self.assertEqual(factor.production_data_format, OutputDataFormat.MULTI_INDEX_DF)
        self.assertEqual(factor.freq, FreqType.EOM)

        index = pd.MultiIndex.from_product([[dt(2014, 1, 30), dt(2014, 2, 28), dt(2014, 3, 31)], ['001', '002']],
                                           names=['tradeDate', 'secID'])
        factor_data_expected = pd.DataFrame(index=index, data=[1, 2, 3, 4, 5, 6], columns=['test'])
        assert_frame_equal(factor.data, factor_data_expected)

    def test_factor_3(self):
        """
        test index name validation 
        """
        index = pd.MultiIndex.from_product([[dt(2014, 1, 30), dt(2014, 2, 28), dt(2014, 3, 31)], ['001', '002']],
                                           names=['date', 'sec'])
        data = pd.DataFrame(index=index, data=[1, 2, 3, 4, 5, 6])
        factor = Factor(data=data, name='test2')
        index_exp = pd.MultiIndex.from_product([[dt(2014, 1, 30), dt(2014, 2, 28), dt(2014, 3, 31)], ['001', '002']],
                                               names=['tradeDate', 'secID'])

        expected = pd.DataFrame(index=index_exp, data=[1, 2, 3, 4, 5, 6], columns=['test2'])
        assert_frame_equal(factor.data, expected)

    def test_factor_container_1(self):
        index = pd.MultiIndex.from_product([['2014-01-30', '2014-02-28', '2014-03-31'], ['001', '002']],
                                           names=['tradeDate', 'secID'])
        data1 = pd.DataFrame(index=index, data=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        factor_test1 = Factor(data=data1, name='test1')

        data2 = pd.DataFrame(index=index, data=[3.0, 2.0, 3.0, 7.0, 8.0, 9.0])
        factor_test2 = Factor(data=data2, name='test2')

        data3 = pd.DataFrame(index=index, data=[3.0, 4.0, 3.0, 5.0, 6.0, 7.0])
        factor_test3 = Factor(data=data3, name='test3')

        fc = FactorContainer('2014-01-30', '2014-02-28', [factor_test1, factor_test2])

        index_exp = pd.MultiIndex.from_product([[dt(2014, 1, 30), dt(2014, 2, 28)], ['001', '002']],
                                               names=['tradeDate', 'secID'])

        data_exp = pd.DataFrame({'test1': [1.0, 2.0, 3.0, 4.0], 'test2': [3.0, 2.0, 3.0, 7.0]}, index=index_exp)
        assert_frame_equal(fc.data, data_exp)

        fc.add_factor(factor_test3)
        data_exp = pd.DataFrame({'test1': [1.0, 2.0, 3.0, 4.0], 'test2': [3.0, 2.0, 3.0, 7.0],
                                 'test3': [3.0, 4.0, 3.0, 5.0]}, index=index_exp)
        assert_frame_equal(fc.data, data_exp)

        fc.remove_factor(factor_test2)
        data_exp = pd.DataFrame({'test1': [1.0, 2.0, 3.0, 4.0], 'test3': [3.0, 4.0, 3.0, 5.0]}, index=index_exp)
        assert_frame_equal(fc.data, data_exp)

        property_exp = {'test1': {'type': FactorType.ALPHA_FACTOR,
                                  'data_format': OutputDataFormat.MULTI_INDEX_DF,
                                  'norm_type': FactorNormType.Null,
                                  'freq': FreqType.EOM},
                        'test3': {'type': FactorType.ALPHA_FACTOR,
                                  'data_format': OutputDataFormat.MULTI_INDEX_DF,
                                  'norm_type': FactorNormType.Null,
                                  'freq': FreqType.EOM}}
        self.assertEqual(fc.property, property_exp)

        fc.replace_data(np.array([[1.0, 2.0, 3.0, 4.0], [1.0, 2.0, 3.0, 5.0]]).T)
        assert_frame_equal(fc.data,
                           pd.DataFrame({'test1': [1.0, 2.0, 3.0, 4.0], 'test3': [1.0, 2.0, 3.0, 5.0]},
                                        index=index_exp))

        self.assertEqual(fc.alpha_factor_col, ['test1', 'test3'])
