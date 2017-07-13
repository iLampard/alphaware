# -*- coding: utf-8 -*-


from unittest import TestCase
import pandas as pd
from pandas.util.testing import assert_frame_equal
from datetime import datetime as dt
from alphaware.base import (Factor,
                                  FactorContainer)
from alphaware.preprocess import FactorStandardizer
from alphaware.enums import FactorType


class TestStandardizer(TestCase):
    def test_standardizer(self):
        index = pd.MultiIndex.from_product([['2014-01-30', '2014-02-28'], ['001', '002', '003', '004']],
                                           names=['date', 'secID'])
        data1 = pd.DataFrame(index=index, data=[1.0, 1.0, 1.2, 200.0, 0.9, 5.0, 5.0, 5.1])
        factor_test1 = Factor(data=data1, name='test1')

        data2 = pd.DataFrame(index=index, data=[2.6, 2.5, 2.8, 2.9, 2.7, 1.9, -10.0, 2.1])
        factor_test2 = Factor(data=data2, name='test2')

        data3 = pd.DataFrame(index=index, data=['a', 'b', 'a', 'd', 'a', 'b', 'c', 'b'])
        factor_test3 = Factor(data=data3, name='test3', property_dict={'type': FactorType.INDUSTY_CODE})

        fc = FactorContainer('2014-01-30', '2014-02-28', [factor_test1, factor_test2, factor_test3])
        calculated = FactorStandardizer().fit_transform(fc)
        index = pd.MultiIndex.from_product([[dt(2014, 1, 30), dt(2014, 2, 28)], ['001', '002', '003', '004']],
                                           names=['date', 'secID'])
        expected = pd.DataFrame({'test1': [-0.578123937458, -0.578123937458, -0.575802154576, 1.73205002949,
                                           -1.73160039778, 0.558580773478, 0.558580773478, 0.614438850826],
                                 'test2': [-0.632455532034, -1.26491106407, 0.632455532034, 1.26491106407,
                                           0.664422038189, 0.513631221012, -1.72938218451, 0.551328925306],
                                 'test3': ['a', 'b', 'a', 'd', 'a', 'b', 'c', 'b']},
                                index=index,
                                dtype=object)
        assert_frame_equal(calculated, expected)
