# -*- coding: utf-8 -*-


from unittest import TestCase
import pandas as pd
import numpy as np
from numpy.testing import (assert_array_equal,
                           assert_array_almost_equal)
from pandas.util.testing import assert_frame_equal
from datetime import datetime as dt
from alphaware.base import (Factor,
                            FactorContainer)
from alphaware.preprocess import (get_indicator_matrix,
                                  Neutralizer,
                                  FactorNeutralizer)
from alphaware.enums import (FactorType,
                             FactorNormType)


class TestNeutralizer(TestCase):
    def setUp(self):
        index = ['001', '002', '003', '004', '005', '006', '007', '008', '009', '010']
        factor = [24, 1.0, 1.1, 0.8, 0.5, 1.2, -1.0, -2, 1.0, 0.5]
        industry = ['a', 'a', 'b', 'c', 'b', 'b', 'b', 'b', 'c', 'c']
        cap = [2.0, 2.0, 1.0, 3.0, 5.0, 1.0, 1.0, 1.0, 1.0, 2.0]
        pd_factor = pd.Series(factor, index=index, name='factor')
        pd_industry = pd.Series(industry, index=index)
        pd_cap = pd.Series(cap, index=index)

        self.data = {'factor': pd_factor,
                     'industry': pd_industry,
                     'cap': pd_cap,
                     'np_factor': np.array(factor),
                     'np_industry': np.array(industry),
                     'np_cap': np.array(cap)}

    def test_get_indicator_matrix(self):
        industry = self.data['industry']
        calculated = get_indicator_matrix(industry)
        expected = np.array([[1.0, 0.0, 0.0],
                             [1.0, 0.0, 0.0],
                             [0.0, 1.0, 0.0],
                             [0.0, 0.0, 1.0],
                             [0.0, 1.0, 0.0],
                             [0.0, 1.0, 0.0],
                             [0.0, 1.0, 0.0],
                             [0.0, 1.0, 0.0],
                             [0.0, 0.0, 1.0],
                             [0.0, 0.0, 1.0]])
        assert_array_equal(calculated, expected)

        industry = self.data['industry']
        cap = self.data['cap']
        calculated = get_indicator_matrix(industry, cap)
        expected = np.array([[1.0, 0.0, 0.0, 2.0],
                             [1.0, 0.0, 0.0, 2.0],
                             [0.0, 1.0, 0.0, 1.0],
                             [0.0, 0.0, 1.0, 3.0],
                             [0.0, 1.0, 0.0, 5.0],
                             [0.0, 1.0, 0.0, 1.0],
                             [0.0, 1.0, 0.0, 1.0],
                             [0.0, 1.0, 0.0, 1.0],
                             [0.0, 0.0, 1.0, 1.0],
                             [0.0, 0.0, 1.0, 2.0]])
        assert_array_equal(calculated, expected)

    def test_neutralizer(self):
        industry = self.data['industry']
        factor = self.data['factor']
        calculated = Neutralizer(industry=industry).fit_transform(factor)
        expected = np.array(
            [11.5, -11.5, 1.14, 0.0333333333333, 0.54, 1.24, -0.96, -1.96, 0.233333333333, -0.266666666667])
        assert_array_almost_equal(calculated, expected)

        industry = self.data['industry']
        factor = self.data['factor']
        cap = self.data['cap']
        calculated = Neutralizer(industry, cap).fit_transform(factor)
        expected = np.array(
            [11.5, -11.5, 1.22627682982, -0.101047981403, 0.194892680726, 1.32627682982, -0.873723170181,
             -1.87372317018, 0.393417510971, -0.292369529568])
        assert_array_almost_equal(calculated, expected)

        industry = self.data['np_industry']
        factor = self.data['np_factor']
        cap = self.data['np_cap']
        calculated = Neutralizer(industry, cap).fit_transform(factor)
        expected = np.array(
            [11.5, -11.5, 1.22627682982, -0.101047981403, 0.194892680726, 1.32627682982, -0.873723170181,
             -1.87372317018, 0.393417510971, -0.292369529568])
        assert_array_almost_equal(calculated, expected)

    def test_factor_neutralizer(self):
        index = pd.MultiIndex.from_product([['2014-01-30', '2014-02-28'], ['001', '002', '003', '004']],
                                           names=['trade_date', 'ticker'])
        data1 = pd.DataFrame(index=index, data=[1.0, 1.0, 1.2, 2.0, 0.9, 5.0, 5.0, 5.1])
        factor_test1 = Factor(data=data1, name='test1',
                              property_dict={'norm_type': FactorNormType.Industry_Cap_Neutral})

        data2 = pd.DataFrame(index=index, data=[2.6, 2.5, 2.8, 2.9, 2.7, 1.9, 5.0, 2.1])
        factor_test2 = Factor(data=data2, name='test2', property_dict={'type': FactorType.ALPHA_FACTOR_MV,
                                                                       'norm_type': FactorNormType.Industry_Neutral})

        data3 = pd.DataFrame(index=index, data=['a', 'b', 'a', 'a', 'a', 'b', 'c', 'b'])
        factor_test3 = Factor(data=data3, name='test3', property_dict={'type': FactorType.INDUSTY_CODE})

        data4 = pd.DataFrame(index=index, data=[1.0, 1.0, 1.2, 2.0, 0.9, 5.0, 5.0, 5.1])
        factor_test4 = Factor(data=data4, name='test4', property_dict={'norm_type': FactorNormType.Industry_Neutral})

        fc = FactorContainer('2014-01-30', '2014-02-28', [factor_test1, factor_test2, factor_test3, factor_test4])

        calculated = FactorNeutralizer().fit_transform(fc)
        index = pd.MultiIndex.from_product([[dt(2014, 1, 30), dt(2014, 2, 28)], ['001', '002', '003', '004']],
                                           names=['trade_date', 'ticker'])
        expected = pd.DataFrame({'test1': [0.0983574180639, 8.881784197e-16, -0.306074564019, 0.207717145955,
                                           -2.10942374679e-15, 8.881784197e-16, -5.3290705182e-15, 0.0],
                                 'test2': [-0.166666666667, 0.0, 0.0333333333333, 0.133333333333, 0.0, -0.1, 0.0, 0.1],
                                 'test3': ['a', 'b', 'a', 'a', 'a', 'b', 'c', 'b'],
                                 'test4': [-0.4, 0.0, -0.2, 0.6, 0.0, -0.05, 0.0, 0.05]},
                                index=index,
                                dtype=object)
        assert_frame_equal(calculated, expected)

        calculated = FactorNeutralizer(out_container=True).fit_transform(fc)
        assert_frame_equal(calculated.data, expected)
        self.assertEqual(calculated.container_property, fc.container_property)
