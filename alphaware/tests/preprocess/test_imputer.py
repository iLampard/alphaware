# -*- coding: utf-8 -*-

from unittest import TestCase
import pandas as pd
from pandas.util.testing import assert_frame_equal
from toolz import merge
import numpy as np
from datetime import datetime as dt
from numpy.testing import assert_array_equal
from alphaware.preprocess import (ExtCategoricalImputer,
                                  FactorImputer,
                                  Factor,
                                  FactorContainer)
from alphaware.enums import (NAStrategy,
                             FactorType)


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


class TestFactorImputer(TestCase):
    def test_imputer_1(self):
        index = pd.MultiIndex.from_product([['2014-01-30', '2014-02-28'], ['001', '002', '003', '004']],
                                           names=['tradeDate', 'secID'])
        data1 = pd.DataFrame(index=index, data=[1.0, 3.0, 3.0, np.nan, 5.0, 5.0, 6.0, 8.0])
        factor_test1 = Factor(data=data1, name='test1')

        data2 = pd.DataFrame(index=index, data=[3.0, 2.0, 3.0, 7.0, 7.0, np.nan, 6.0, 6.0])
        factor_test2 = Factor(data=data2, name='test2')

        data3 = pd.DataFrame(index=index, data=[3.0, 3.0, np.nan, 5.0, 6.0, 7.0, 6.0, 6.0])
        factor_test3 = Factor(data=data3, name='test3')

        fc = FactorContainer('2014-01-30', '2014-02-28', [factor_test1, factor_test2, factor_test3])

        index = pd.MultiIndex.from_product([[dt(2014, 1, 30), dt(2014, 2, 28)], ['001', '002', '003', '004']],
                                           names=['tradeDate', 'secID'])
        calculated = FactorImputer(numerical_strategy=NAStrategy.MOST_FREQ).fit_transform(fc)
        expected = pd.DataFrame({'test1': [1.0, 3.0, 3.0, 3.0, 5.0, 5.0, 6.0, 8.0],
                                 'test2': [3.0, 2.0, 3.0, 7.0, 7.0, 6.0, 6.0, 6.0],
                                 'test3': [3.0, 3.0, 3.0, 5.0, 6.0, 7.0, 6.0, 6.0]},
                                index=index)
        assert_frame_equal(calculated, expected)

        calculated = FactorImputer(numerical_strategy=NAStrategy.MEDIAN).fit_transform(fc)
        expected = pd.DataFrame({'test1': [1.0, 3.0, 3.0, 3.0, 5.0, 5.0, 6.0, 8.0],
                                 'test2': [3.0, 2.0, 3.0, 7.0, 7.0, 6.0, 6.0, 6.0],
                                 'test3': [3.0, 3.0, 3.0, 5.0, 6.0, 7.0, 6.0, 6.0]},
                                index=index)
        assert_frame_equal(calculated, expected)

        industry = pd.DataFrame(index=index, data=['a', 'a', 'a', 'a', 'a', 'a', np.nan, 'a'])
        factor_industry = Factor(data=industry, name='industry', property_dict={'type': FactorType.INDUSTY_CODE})
        fc.add_factor(factor=factor_industry)
        calculated = FactorImputer(numerical_strategy=NAStrategy.MEDIAN,
                                   categorical_strategy=NAStrategy.CUSTOM,
                                   custom_value='other').fit_transform(fc)
        calculated.sort_index(axis=1, inplace=True)
        expected = pd.DataFrame({'test1': [1.0, 3.0, 3.0, 3.0, 5.0, 5.0, 6.0, 8.0],
                                 'test2': [3.0, 2.0, 3.0, 7.0, 7.0, 6.0, 6.0, 6.0],
                                 'test3': [3.0, 3.0, 3.0, 5.0, 6.0, 7.0, 6.0, 6.0],
                                 'industry': ['a', 'a', 'a', 'a', 'a', 'a', 'other', 'a']},
                                index=index,
                                dtype=object)
        assert_frame_equal(calculated, expected)

    def test_imputer_2(self):
        index = pd.MultiIndex.from_product([['2014-01-30', '2014-02-28'], ['001', '002', '003', '004']],
                                           names=['tradeDate', 'secID'])
        data = pd.DataFrame(index=index, data=[1.0, 3.0, 3.0, np.nan, 5.0, 5.0, 6.0, 8.0])
        factor_test = Factor(data=data, name='test1')

        index = pd.MultiIndex.from_product([[dt(2014, 1, 30), dt(2014, 2, 28)], ['001', '002', '003', '004']],
                                           names=['tradeDate', 'secID'])
        fi = FactorImputer(numerical_strategy=NAStrategy.MEAN, groupby_date=False)
        calculated = fi.fit_transform(factor_test)
        expected = pd.DataFrame({'test1': [1.0, 3.0, 3.0, 4.428571, 5.0, 5.0, 6.0, 8.0]}, index=index)
        assert_frame_equal(calculated, expected)

        fi.set_out_container(True)
        calculated = fi.fit_transform(factor_test)
        expected = FactorContainer(start_date='2014-01-30',
                                   end_date='2014-02-28')
        factor = Factor(data=pd.DataFrame({'test1': [1.0, 3.0, 3.0, 4.428571, 5.0, 5.0, 6.0, 8.0]}, index=index),
                        name='test1')
        expected.add_factor(factor)

        assert (isinstance(calculated, FactorContainer))
        self.assertEqual(calculated.property, expected.property)
        assert_frame_equal(calculated.data, expected.data)
